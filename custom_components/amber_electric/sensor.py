"""Amber Electric Sensor"""
from datetime import datetime, timedelta
import logging

import voluptuous as vol

from homeassistant.const import (
    ATTR_UNIT_OF_MEASUREMENT,
    DEVICE_CLASS_ENERGY,
    ENERGY_KILO_WATT_HOUR,
    CONF_NAME,
    EVENT_HOMEASSISTANT_START,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
)
from homeassistant.core import callback
from homeassistant.helpers import entity_platform
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.event import (
    async_track_state_change_event,
    async_track_time_change,
)
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.typing import HomeAssistantType


from .const import (
    DOMAIN,
    CURRENCY_AUD,
    LOSS_FACTOR,
    AMBER_DAILY_PRICE,
    GREEN_KWH_PRICE,
    LOSS_FACTOR,
    MARKET_KWH_PRICE,
    NETWORK_DAILY_PRICE,
    NETWORK_KWH_PRICE,
    OFFSET_KWH_PRICE,
    TOTAL_DAILY_PRICE,
    TOTAL_FIXED_KWH_PRICE,
    MANUFACTURER,
)


_LOGGER = logging.getLogger(__name__)

DEFAULT_SCAN_INTERVAL = timedelta(seconds=30)
SCAN_INTERVAL = DEFAULT_SCAN_INTERVAL


async def async_setup_entry(hass: HomeAssistantType, entry, async_add_entities):
    """Configure a dispatcher connection based on a config entry."""

    api = hass.data[DOMAIN][entry.entry_id]

    if not "entity_ref" in hass.data[DOMAIN]:
        hass.data[DOMAIN]["entity_ref"] = {}

    if not "tasks" in hass.data[DOMAIN]:
        hass.data[DOMAIN]["tasks"] = {}

    hass.data[DOMAIN]["entity_ref"][
        f"{api.postcode}_usage"
    ] = AmberElectricUsagePriceSensor(price_type="USAGE", api=api)
    hass.data[DOMAIN]["entity_ref"][
        f"{api.postcode}_export"
    ] = AmberElectricUsagePriceSensor(price_type="EXPORT", api=api)
    hass.data[DOMAIN]["entity_ref"][
        f"{api.postcode}_market_consumption"
    ] = AmberElectricMarketConsumption(api=api)

    def device_event_handler(event_data):
        if not (event_data):
            _LOGGER.warning("Event received with no event data")
            return None
        _LOGGER.debug("Update event received")

        for entity_id in hass.data[DOMAIN]["entity_ref"]:
            try:
                hass.data[DOMAIN]["entity_ref"][entity_id].async_device_changed()
            except Exception as err:
                _LOGGER.error("Unable to send update to HA")
                _LOGGER.exception(err)
                raise err

    entities = list()
    for entity_id in hass.data[DOMAIN]["entity_ref"]:
        _LOGGER.debug(
            "Adding entity %s (%s) to list with state: %s",
            hass.data[DOMAIN]["entity_ref"][entity_id].name,
            hass.data[DOMAIN]["entity_ref"][entity_id].unique_id,
            hass.data[DOMAIN]["entity_ref"][entity_id].state,
        )
        entities.append(hass.data[DOMAIN]["entity_ref"][entity_id])

    async_add_entities(entities)

    hass.data[DOMAIN]["tasks"]["update_tracker"] = api.poll_for_updates(
        interval=SCAN_INTERVAL, event_receiver=device_event_handler
    )


class AmberElectricMarketConsumption(RestoreEntity):
    """Represent Amber Electric Market Consumption Data."""

    def __init__(self, price_type="USAGE", api=None):
        """Set up Amber Electric Market Consumption Entity."""
        super().__init__()
        self.__api = api
        self.__period = api.market.variable.periods[0]
        self.__name = f"{self.__api.postcode} Market Consumption"
        self.__id = f"{self.__api.postcode}_market_onsumption"

    def async_device_changed(self):
        """Send changed data to HA"""
        _LOGGER.debug("%s (%s) advising HA of update", self.name, self.unique_id)
        self.async_schedule_update_ha_state()

    @property
    def state(self):
        return self.__period.operational_demand

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return ENERGY_KILO_WATT_HOUR

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return DEVICE_CLASS_ENERGY

    @property
    def device_info(self):
        """Return the device_info of the device."""
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": self.name,
            "model": f"Market Consumption",
            "sw_version": None,
            "manufacturer": MANUFACTURER,
        }

    @property
    def should_poll(self):
        return False

    @property
    def icon(self):
        return "mdi:flash"

    @property
    def device_state_attributes(self):
        """Return device specific attributes."""
        data = dict()
        # "created_at": "2020-10-07T12:04:41+10:00",
        # "operational_demand": 7192.31,
        # "percentile_rank": 0.45,
        # "period": "2020-10-06T12:30:00+10:00",
        # "period_source": 1800.0,
        # "period_type": "ACTUAL",
        # "region": "NSW1",
        # "renewables_percentage": 0.23648912556801402,
        # "rooftop_solar": 1205.37,
        # "semi_scheduled_generation": 780.59,
        # "ts": 1601951400.0,
        # "wholesale_kwh_price": 0.05534
        # data[LOSS_FACTOR] = self.__ancillary_data.loss_factor
        # data[AMBER_DAILY_PRICE] = self.__ancillary_data.amber_daily_price
        # data[GREEN_KWH_PRICE] = self.__ancillary_data.green_kwh_price
        # data[LOSS_FACTOR] = self.__ancillary_data.loss_factor
        # data[MARKET_KWH_PRICE] = self.__ancillary_data.market_kwh_price
        # data[NETWORK_DAILY_PRICE] = self.__ancillary_data.network_daily_price
        # data[NETWORK_KWH_PRICE] = self.__ancillary_data.network_kwh_price
        # data[OFFSET_KWH_PRICE] = self.__ancillary_data.offset_kwh_price
        # data[TOTAL_DAILY_PRICE] = self.__ancillary_data.total_daily_price
        # data[TOTAL_FIXED_KWH_PRICE] = self.__ancillary_data.total_fixed_kwh_price
        return data

    @property
    def name(self):
        """Return the name of the device."""
        return self.__name

    @property
    def unique_id(self):
        """Return the unique ID."""
        return self.__id

    async def async_update(self):
        """Update Trackimo Data"""
        await self.__api.market.update()

    async def async_added_to_hass(self):
        """Register state update callback."""
        await super().async_added_to_hass()

    async def async_will_remove_from_hass(self):
        """Clean up after entity before removal."""
        await super().async_will_remove_from_hass()


class AmberElectricPriceSensor(RestoreEntity):
    """Represent a Amber Electric pricing."""

    def __init__(self, price_type="USAGE", api=None):
        """Set up Amber Electric pricing."""
        super().__init__()
        self.__api = api
        self.__price_type = price_type
        if self.__price_type == "USAGE":
            self.__price = api.market.usage_price
            self.__ancillary_data = api.market.e1
            self.__name = f"{self.__api.postcode} usage market rate"
            self.__id = f"{self.__api.postcode}_usage_market"
        elif self.__price_type == "EXPORT":
            self.__price = api.market.export_price
            self.__ancillary_data = api.market.b1
            self.__name = f"{self.__api.postcode} export market rate"
            self.__id = f"{self.__api.postcode}_export_market"
        else:
            _LOGGER.error("Unknown price type: %s", price_type)

    def async_device_changed(self):
        """Send changed data to HA"""
        _LOGGER.debug("%s (%s) advising HA of update", self.name, self.unique_id)
        self.async_schedule_update_ha_state()

    @property
    def state(self):
        return self.__price

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return CURRENCY_AUD

    @property
    def device_info(self):
        """Return the device_info of the device."""
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": self.name,
            "model": f"Market {self.__price_type}",
            "sw_version": None,
            "manufacturer": MANUFACTURER,
        }

    @property
    def should_poll(self):
        return False

    @property
    def icon(self):
        return "mdi:currency-usd"

    @property
    def device_state_attributes(self):
        """Return device specific attributes."""
        data = dict()
        data[LOSS_FACTOR] = self.__ancillary_data.loss_factor
        data[AMBER_DAILY_PRICE] = self.__ancillary_data.amber_daily_price
        data[GREEN_KWH_PRICE] = self.__ancillary_data.green_kwh_price
        data[LOSS_FACTOR] = self.__ancillary_data.loss_factor
        data[MARKET_KWH_PRICE] = self.__ancillary_data.market_kwh_price
        data[NETWORK_DAILY_PRICE] = self.__ancillary_data.network_daily_price
        data[NETWORK_KWH_PRICE] = self.__ancillary_data.network_kwh_price
        data[OFFSET_KWH_PRICE] = self.__ancillary_data.offset_kwh_price
        data[TOTAL_DAILY_PRICE] = self.__ancillary_data.total_daily_price
        data[TOTAL_FIXED_KWH_PRICE] = self.__ancillary_data.total_fixed_kwh_price
        return data

    @property
    def name(self):
        """Return the name of the device."""
        return self.__name

    @property
    def unique_id(self):
        """Return the unique ID."""
        return self.__id

    async def async_update(self):
        """Update Trackimo Data"""
        await self.__api.market.update()

    async def async_added_to_hass(self):
        """Register state update callback."""
        await super().async_added_to_hass()

    async def async_will_remove_from_hass(self):
        """Clean up after entity before removal."""
        await super().async_will_remove_from_hass()


class AmberElectricUsagePriceSensor(AmberElectricPriceSensor):
    pass


class AmberElectricExportPriceSensor(AmberElectricPriceSensor):
    pass