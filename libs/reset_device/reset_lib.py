import os

def reset_to_host_mode():
	os.system('aplay /usr/lib/raspi-wifi/reset_device/button_chime.wav')
	os.system('sudo rm -f /etc/wpa_supplicant/wpa_supplicant.conf')
	os.system('sudo rm -f /home/pi/Projects/RaspiWifi/tmp/*')
	os.system('sudo rm /etc/cron.raspiwifi/apclient_bootstrapper')
	os.system('sudo cp -r /usr/lib/raspi-wifi/reset_device/static_files/aphost_bootstrapper /etc/cron.raspiwifi/')
	os.system('chmod +x /etc/cron.raspiwifi/aphost_bootstrapper')
	os.system('sudo mv /etc/dhcpcd.conf /etc/dhcpcd.conf.original')
	os.system('sudo cp -r /usr/lib/raspi-wifi/reset_device/static_files/dhcpcd.conf /etc/')
	os.system('sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.original')
	os.system('sudo cp -r /usr/lib/raspi-wifi/reset_device/static_files/dnsmasq.conf /etc/')
	os.system('sudo cp -r /usr/lib/raspi-wifi/reset_device/static_files/dhcpcd.conf /etc/')
	os.system('sudo reboot')
