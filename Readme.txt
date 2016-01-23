This code was written to configure a Raspberry Pi device for wireless access when no display is 
available (very similar to the way a Chromecast or similar device needs to be configured).

For now some of the paths are hard-coded so the project should be run from 
/home/pi/Projects/RaspiWifi/ You can, of course change that location but make
sure to update all hard links to that location in the source files before running.

Although this app was devleoped for use with the Raspberry Pi and the Edimax EW-7811Un USB WiFi 
adapter, the only Raspberry Pi specific code would be the GPIO call to watch for a physical 
reset button to be pressed for 10 seconds.



Software Requirements:

Ruby on Rails 4.2.0
isc-dhcp-server
hostapd