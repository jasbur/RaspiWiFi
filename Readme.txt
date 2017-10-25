RaspiWiFi

RaspiWiFi is a program to headlessly configure a Raspberry Pi's WiFi 
connection using using any other WiFi-enabled device (much like the way 
a Chromecast or similar device can be configured). RaspiWiFi has been 
tested with the Raspberry Pi B+, Raspberry Pi 3, and Raspberry Pi Zero W.



INSTALLATION INSTRUCTIONS:

== Navigate to the directory you downloaded or cloned RaspiWiFi to

== Run:

sudo python3 initial_setup.py

== This script will install all necessary prerequisites, copy configuration files, and reboot. When it finishes booting it should present itself in "Configuration Mode" as a WiFi access point with the name "RaspiWiFi Setup".




USAGE:

== Connect to the "RaspiWiFi Setup" access point using any other WiFi enabled device.

== Navigate to http://10.0.0.1 using any web browser on the device you connected with.

== Select the WiFi connection you'd like your Raspberry Pi to connect to from the drop down list and enter its wireless password on the page provided. If no encryption is enabled, leave the password box blank.

== Click the "Connect" button.

== At this point your Raspberry Pi will reboot and connect to the access point specified.




RESETTING THE DEVICE:

== If GPIO 18 is pulled HIGH for 10 seconds or more the Raspberry Pi will reset all settings, reboot, and enter "Configuration Mode" again. It's useful to have a simple button wired on GPIO 18 to reset easily if moving to a new location, or if incorrect connection information is ever entered. Just press and hold for 10 seconds or longer.

== You can also reset the device by re-running the initial_setup.py as instructed above.
