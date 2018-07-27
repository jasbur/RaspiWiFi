RaspiWiFi

RaspiWiFi is a program to headlessly configure a Raspberry Pi's WiFi
connection using using any other WiFi-enabled device (much like the way
a Chromecast or similar device can be configured).

It can also be used as a method to connect wirelessly point-to-point with your
Pi when a network is not available or you do not want to connect to one. Just
leave it in Configuration Mode, connect to the "RaspiWiFi[xxxx] Setup" access
point. The Pi will be addressable at 10.0.0.1 using all the normal methods you
might use while connected through a network.

RaspiWiFi has been
tested with the Raspberry Pi B+, Raspberry Pi 3, and Raspberry Pi Zero W.



OS IMAGE USAGE:

== Just burn the ".IMG" file attached to this release to an 8GB+ SD card. Boot
your Raspberry Pi with the SD card and it will automatically boot into its AP
Host (broadcast) mode with an SSID based on a unique id (the last four of your
Pi's serial number). No input devices or displays necessary. Otherwise this is
a base install of the current Raspbian Stretch, up to date as of the date of
this release.



 SCRIPT-BASED INSTALLATION INSTRUCTIONS:

== Navigate to the directory where you downloaded or cloned RaspiWiFi

== Run:

sudo python3 initial_setup.py

== This script will install all necessary prerequisites, copy the project files
to /usr/lib/raspiwifi/, copy configuration
files for AP Host (configuration) mode, and reboot. When it finishes booting it
should present itself in "Configuration Mode" as a WiFi access point with the
name "RaspiWiFi[xxxx] Setup".

== The original RaspiWiFi directory that you ran the Initial Setup is no longer
needed after installation and can be safely deleted. All necessary files are
copied to /usr/lib/raspiwifi/ on setup.


CONFIGURATION:

== You will be prompted to set 3 variables during the Initial Setup Script:

==== "SSID Prefix" [default: "RaspiWiFi Setup"]: This is the prefix of the SSID
      that your Pi will broadcast for you to connect to during
      Configuration Mode (Host Mode). The last four of you Pi's serial number
      will be appended to whatever you enter here.

==== "Auto-Config mode" [default: n]: If you choose to enable this mode your Pi
      will check for an active connection while in normal operation mode (Client Mode).
      If an active connection has been determined to be lost, the Pi will reboot
      back into Configuration Mode (Host Mode) automatically.

==== "Auto-Config delay" [default: 300 seconds]: This is the time in consecutive
      seconds to wait with an inactive connection before triggering a reset into
      Configuration Mode (Host Mode). This is only applicable if the
      "Auto-Config mode" mentioned above is set to active.

==== "SSL Mode" [default: n]: With this option enabled your RaspiWifi
      configuration page will be sent over an SSL encrypted connection (don't
      forget the "s" when navigating to https://10.0.0.1:9191 when using
      this mode). You will get a certificate error from your web browser when
      connecting. The error is just a warning that the certificate has not been
      verified by a third party but everything will be properly encrypted anyway.

== All of these variables can be set at any time after the Initial Setup has
been running by editing the /etc/raspiwifi/raspiwifi.conf


USAGE:

== Connect to the "RaspiWiFi[xxxx] Setup" access point using any other WiFi enabled
device.

== Navigate to http://10.0.0.1:9191 (or https://10.0.0.1:9191 when using SSL
mode) using any web browser on the device you connected with.

== Select the WiFi connection you'd like your Raspberry Pi to connect to from
the drop down list and enter its wireless password on the page provided. If no
encryption is enabled, leave the password box blank.

== Click the "Connect" button.

== At this point your Raspberry Pi will reboot and connect to the access point
specified.

== You can also use the Pi in a point-to-point connection mode by leaving it in
Configuration Mode. All services will be addresible in their normal way at
10.0.0.1 while connected to the "RaspiWiFi[xxxx] Setup" AP.



RESETTING THE DEVICE:

== If GPIO 18 is pulled HIGH for 10 seconds or more the Raspberry Pi will reset
all settings, reboot, and enter "Configuration Mode" again. It's useful to have
a simple button wired on GPIO 18 to reset easily if moving to a new location,
or if incorrect connection information is ever entered. Just press and hold for
10 seconds or longer.

== You can also reset the device by running the manual_reset.py in the
/usr/lib/raspiwifi/reset_device directory as root or with sudo.
