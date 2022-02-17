import RPi.GPIO as GPIO
import os
import time
import subprocess
import reset_lib

def get_serial():
    serial = "UNKN"
    with open("/sys/firmware/devicetree/base/serial-number") as f:
        serial = f.read()
    return serial.replace("\x00", "")


GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 0
serial_last_four = get_serial()[-4:]
config_hash = reset_lib.config_file_hash()
ssid_prefix = config_hash['ssid_prefix'] + " "

wpa_changed = reset_lib.wpa_check_activate(config_hash['wpa_enabled'] == "1", config_hash['wpa_key'])

ssid_changed = reset_lib.update_ssid(ssid_prefix, serial_last_four)

reboot_required = wpa_changed or ssid_changed

if reboot_required:
    print("Rebooting, wpa_changed = {}, ssid_changed = {}", wpa_changed, ssid_changed)
    os.system('reboot')

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
