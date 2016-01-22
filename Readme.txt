This code was written to configure a Raspberry Pi device for wireless access when no display is available (very similar to the way a Chromecast or similar device needs to be configured).

For now some of the paths are hard-coded so the contents of the "Reset Device" folder should be copied directly into the /home/pi/ directory. The contents of the "Configuration App" folder should be copied to /home/pi/wifi_setup_app/

Although this app was devleoped for use with the Raspberry Pi and the Edimax EW-7811Un USB WiFi adapter, the only Raspberry Pi specific code would be the Pi_Piper call the watch for a physical reset button to be pressed for 10 seconds.



Software Requirements:

Ruby on Rails 4.2.0
dsnmasq
hostapd