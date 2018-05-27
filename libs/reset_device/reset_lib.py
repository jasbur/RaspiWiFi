import os
import fileinput
import subprocess

def config_file_hash():
	config_file = open('/etc/raspiwifi/raspiwifi.conf')
	config_hash = {}

	for line in config_file:
		line_key = line.split("=")[0]
		line_value = line.split("=")[1].rstrip()
		config_hash[line_key] = line_value

	return config_hash

def hostapd_reset_check(ssid_prefix):
	hostapd_conf = open('/etc/hostapd/hostapd.conf', 'r')
	reset_required = True

	for line in hostapd_conf:
	    if ssid_prefix in line:
	        reset_required = False

	return reset_required

def update_hostapd(ssid_prefix, serial_last_four):
	os.system('cp -a /usr/lib/raspiwifi/reset_device/static_files/hostapd.conf /etc/hostapd/')

	with fileinput.FileInput("/etc/hostapd/hostapd.conf", inplace=True) as file:
		for line in file:
			print(line.replace("temp-ssid", ssid_prefix + serial_last_four), end='')
			file.close

def is_wifi_active():
	iwconfig_out = subprocess.check_output(['iwconfig']).decode('utf-8')
	wifi_active = True

	if "Access Point: Not-Associated" in iwconfig_out:
		wifi_active = False

	return wifi_active

def reset_to_host_mode():
	os.system('aplay /usr/lib/raspiwifi/reset_device/button_chime.wav')
	os.system('rm -f /etc/wpa_supplicant/wpa_supplicant.conf')
	os.system('rm -f /home/pi/Projects/RaspiWifi/tmp/*')
	os.system('rm /etc/cron.raspiwifi/apclient_bootstrapper')
	os.system('cp /usr/lib/raspiwifi/reset_device/static_files/aphost_bootstrapper /etc/cron.raspiwifi/')
	os.system('chmod +x /etc/cron.raspiwifi/aphost_bootstrapper')
	os.system('mv /etc/dhcpcd.conf /etc/dhcpcd.conf.original')
	os.system('cp /usr/lib/raspiwifi/reset_device/static_files/dhcpcd.conf /etc/')
	os.system('mv /etc/dnsmasq.conf /etc/dnsmasq.conf.original')
	os.system('cp /usr/lib/raspiwifi/reset_device/static_files/dnsmasq.conf /etc/')
	os.system('cp /usr/lib/raspiwifi/reset_device/static_files/dhcpcd.conf /etc/')
	os.system('reboot')
