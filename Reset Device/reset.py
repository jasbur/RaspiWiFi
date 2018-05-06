import RPi.GPIO as GPIO
import os
import time
import fileinput
import subprocess
import reset_lib

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 0
serial_last_four = subprocess.check_output(['cat', '/proc/cpuinfo'])[-5:-1].decode('utf-8')
hostapd_conf = open('/etc/hostapd/hostapd.conf', 'r')
ssid_prefix = "RaspiWifi Setup "

# Iterate through the installed hostapd.conf file to assign a device-specific SSID if none has been assigned
for line in hostapd_conf:
    if "temp-ssid" in line:
        with fileinput.FileInput("/etc/hostapd/hostapd.conf", inplace=True) as file:
            for line in file:
                print(line.replace("temp-ssid", ssid_prefix + serial_last_four), end='')
                file.close
        os.system('reboot')
    else:
        hostapd_conf.close

# This is the main logic loop waiting for a button to be pressed on GPIO 18 for 10 seconds.
# If that happens the device will reset to its AP Host mode allowing for reconfiguration on a new network.
while True:
    while GPIO.input(18) == 1:
        time.sleep(1)
        counter = counter + 1

        print(counter)

        if counter == 9:
            reset_lib.reset_to_host_mode()

        if GPIO.input(18) == 0:
            counter = 0
            break

    time.sleep(1)
