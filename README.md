# Amber Electric for Home Assistant

[![GitHub Stars](https://img.shields.io/github/stars/troykelly/hacs-amberelectric.svg)](https://github.com/troykelly/hacs-amberelectric/stargazers) [![GitHub Issues](https://img.shields.io/github/issues/troykelly/hacs-amberelectric.svg)](https://github.com/troykelly/hacs-amberelectric/issues) [![Current Version](https://img.shields.io/badge/version-0.0.12-green.svg)](https://github.com/troykelly/hacs-amberelectric) ![Validate with hassfest](https://github.com/troykelly/hacs-amberelectric/workflows/Validate%20with%20hassfest/badge.svg?branch=master) ![Validate](https://github.com/troykelly/hacs-amberelectric/workflows/Validate/badge.svg)

See electricity damand, renewable generation and pricing for your area courtesy of [Amber Electric](https://www.amberelectric.com.au/).

### Note

The Amber Electric API is returning strange (potentially inaccurate) data at the moment. This information should be as a point of interest, but nothing more. Some day, Amber Electric are releasing a new API - maybe they will fix the issue then. Who knows.

## Live Australian Electricity Pricing

You **do not** need to be an Amber Electric customer to see live pricing for your area.
This integration is great if you have a general interest in electricity pricing or renewables.
Uses your Home Assistant installation location (your latitude and longitude) to select the right electricity market and makes the data available to you to chart and use in automations.

<img width="500" alt="Amber Electric Charts" src="https://user-images.githubusercontent.com/4564803/95395060-754a5380-0949-11eb-8606-c697fa9b0d96.png">

## Sensors

All sensors start with the postcode matched to your electricity market.

### sensor.2044_market_consumption

```yaml
attribution: © Amber Electric Pty Ltd ABN 98 623 603 805
nem_time: "2020-10-08T08:14:17+10:00"
network_provider: Ausgrid
percentile_rank: 0.4431818181818182
period_delta: 300
period_start: "2020-10-08T08:00:00.001000+10:00"
period_end: "2020-10-08T08:30:00+10:00"
period_type: ACTUAL
wholesale_kwh_price: 0.04388999999999999
unit_of_measurement: kWh
friendly_name: 2044 Market Consumption
icon: "mdi:flash"
device_class: energy
```

### sensor.2044_market_solar

```yaml
attribution: © Amber Electric Pty Ltd ABN 98 623 603 805
nem_time: "2020-10-08T08:14:17+10:00"
network_provider: Ausgrid
renewables_percentage: 0.20418
period_delta: 300
period_start: "2020-10-08T08:00:00.001000+10:00"
period_end: "2020-10-08T08:30:00+10:00"
period_type: ACTUAL
unit_of_measurement: kWh
friendly_name: 2044 Market Solar
icon: "mdi:solar-power"
device_class: energy
```

### sensor.2044_export_market_rate

```yaml
attribution: © Amber Electric Pty Ltd ABN 98 623 603 805
nem_time: "2020-10-08T08:14:17+10:00"
network_provider: Ausgrid
loss_factor: -1.04730208
amber_daily_price: 0
green_kwh_price: 0
market_kwh_price: -0.01814440909090909
network_daily_price: 0
network_kwh_price: 0
offset_kwh_price: 0
total_daily_price: 0
total_fixed_kwh_price: -0.018144363636363636
unit_of_measurement: AUD
friendly_name: 2044 export market rate
icon: "mdi:currency-usd"
```

### sensor.2044_usage_market_rate

```yaml
attribution: © Amber Electric Pty Ltd ABN 98 623 603 805
nem_time: "2020-10-08T08:14:17+10:00"
network_provider: Ausgrid
loss_factor: 1.04730208
amber_daily_price: 0.2988792029999999
green_kwh_price: 0.03860999999999999
market_kwh_price: 0.01814545454545454
network_daily_price: 0.3793679999999999
network_kwh_price: 0.08394700000000001
offset_kwh_price: 0.001
total_daily_price: 1.0778125454545455
total_fixed_kwh_price: 0.10309245454545454
unit_of_measurement: AUD
friendly_name: 2044 usage market rate
icon: "mdi:currency-usd"
```

## Buy me a coffee

If this helps you, or you are just generous. I do love coffee.

<a href="https://buymeacoff.ee/troykelly" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>

## Features

- See current network demand
- See current pricing in your area for both consumption and export (solar etc)

## Setup

Install via HACS then...

Add the integration as you would any other via the frontend:

Go to `Integrations` and click the big plus

<img width="89" alt="Big_Orange_Plus" src="https://user-images.githubusercontent.com/4564803/96553770-5fea0780-1301-11eb-80e6-97ec6145ddfb.png">
Click the big plus


Search for Amber Electric
<img width="539" alt="Set_Up_New_Integration" src="https://user-images.githubusercontent.com/4564803/96553776-624c6180-1301-11eb-9fec-e7683c6a1cf5.png">


Just click Submit (you don't have to supply your username and password for market rate data)
<img width="410" alt="Amber_Electric_Username_Password" src="https://user-images.githubusercontent.com/4564803/96553774-611b3480-1301-11eb-8f67-55d2dc3603d9.png">

**[Optionally]** Supply your username and password for Amber Electric to access your pricing and usage data. This is not required for market rates.

## Usage

Once connected, several sensors (see above) will appear with pricing and demand information. They are prefixed with your postcode which is derived from your location.

## Contributions

PR's are more than welcome either to the HACS component or the Amber Electric Library.

### Thanks to:

<a href="https://github.com/hwikene" target="_blank"><img src="https://avatars3.githubusercontent.com/u/17985923?s=460&u=26ef329676c71af07fb01916f4ff553d88bfb94a&v=4" alt="hwikene on GitHub" width="50"/>@hwikene</a> for Norwegian translation

## Data Sources

### Market Electricity Data

Provided by Amber Electric © Amber Electric Pty Ltd ABN 98 623 603 805

### Location to Address Translation

Performed by Open Streetmap © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright
