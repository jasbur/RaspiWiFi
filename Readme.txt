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



USAGE

Just clone this repository to /home/pi/Projects, install the software listed above using apt-get, and copy the
"aphost" files from the "static_files" directory to their appropriate destinations (listed in static_files/README).

Reboot the Raspberry Pi and it will create its own hotspot named "RaspiWifi-Setup". Once connected navigate to 10.0.0.1
from a web browser and setup to connect to your desired wireless network.

Nothing is very optimized at the moment, so booting into the configuration mode can take 2.5 to 3 minutes.