import RPi.GPIO as GPIO
import os
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 0

while True:
    while GPIO.input(18) == 1:
        time.sleep(1)
        counter = counter + 1

        print(counter)

        if counter == 9:
            os.system('aplay [[project_dir]]/Reset\ Device/button_chime.wav')
            os.system('sudo rm -f /etc/wpa_supplicant/wpa_supplicant.conf')
            os.system('rm -f /home/pi/Projects/RaspiWifi/tmp/*')
            os.system('sudo cp -r [[project_dir]]/Reset\ Device/static_files/dhcpd.conf /etc/dhcp/')
            os.system('sudo cp -r [[project_dir]]/Reset\ Device/static_files/hostapd.conf /etc/hostapd/')
            os.system('sudo cp -r [[project_dir]]/Reset\ Device/static_files/interfaces.aphost /etc/network/interfaces')
            os.system('sudo cp -r [[project_dir]]/Reset\ Device/static_files/isc-dhcp-server.aphost /etc/default/isc-dhcp-server')
            os.system('sudo cp -r [[project_dir]]/Reset\ Device/static_files/rc.local.aphost /etc/rc.local')
            os.system('sudo reboot')

        if GPIO.input(18) == 0:
            counter = 0
            break

    time.sleep(1)
