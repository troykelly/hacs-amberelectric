{% if installed %}

## Changes as compared to your installed version:

### Breaking Changes

### Changes

### Features

{% if version_installed.replace("v", "").replace(".","") | int < 20  %}

- Added Norwegian translation from @hwikene
  {% endif %}
  {% if version_installed.replace("v", "").replace(".","") | int < 19  %}
- Removed incompatible requirement
  {% endif %}
  {% if version_installed.replace("v", "").replace(".","") | int < 18  %}
- Explicitly listing requirements
  {% endif %}
  {% if version_installed.replace("v", "").replace(".","") | int < 13  %}
- Fixing issue with Trackimo API force logging out accounts
  {% endif %}
  {% if version_installed.replace("v", "").replace(".","") | int < 7  %}
- Device firmware and details available to interface
  {% endif %}
  {% if version_installed.replace("v", "").replace(".","") | int < 4  %}
- Updated trackimo library to 0.1.16
  {% endif %}
  {% if version_installed.replace("v", "").replace(".","") | int < 3  %}
- Updated trackimo library to 0.1.15
  {% endif %}
  {% if version_installed.replace("v", "").replace(".","") | int < 2  %}
- Updated trackimo library to 0.1.13
  {% endif %}

### Bugfixes

{% if version_installed.replace("v", "").replace(".","") | int < 3  %}

- Fix for authorisation token refresh
  {% endif %}

---

{% endif %}
