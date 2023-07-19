# OTA Wifi Configuration

OTA Wifi Configuration is a program to headlessly configure a Raspberry Pi's WiFi
connection using using any other WiFi-enabled device (much like the way
a Chromecast or similar device can be configured).

### RaspiWiFi has been tested with

-   Raspberry Pi 4b Running Raspberry Pi Os Buster Lite

### RaspiWiFi should work with

-   Any rasberry Pi running Raspberry Pi Os Buster or Bullseye

## Installation Instructions:

-   Navigate to the directory where you downloaded or cloned RaspiWiFi

-   Run: `sudo python3 setup.py`, **Must be run with sudo or as root**

-   This script will install all necessary prerequisites and copy all necessary
    config and library files, then reboot. When it finishes booting it should
    present itself in _Configuration Mode_ as a WiFi access point with the
    name **Device [xxxx]**. The Xs being replaced with the last four digits of your raspberry pi's serial number.

## Usage:

-   Connect to the "Device [xxxx] Setup" access point using any other WiFi enabled
    device.

-   Make an http request to [**192.168.50.10**] or [**setup.com**] on port 80

## Api:

### **/connected** - Attempts to set the wifi on the device. It will set the credentials then restart the device. Will return a 200 status code if succeeded.

-   **Params** - The params must be passed in as JSON data. Mimetype must indicate JSON (application/json).
    -   **SSID** - String - The ssid of the wifi you wish to connect to.
    -   **wifi_key** - String - The wpa key of the wifi you wish to connect to.
-   **Returns** - **{"status": "success", "status_code": 200}** if succeeded or **{"status": "failed", "status_code": 500}** if failed

### **/save_credentials** - will return a 200 status code if succeeded.

-   **Params** - None
-   **Returns** - {"status_code": 200}

## Resetting the device:

### You can reset the device by running setup.py again as root or with sudo.

## Stopping access point

## You can disable the access point by running disable_access_point.py as root or with sudo.
