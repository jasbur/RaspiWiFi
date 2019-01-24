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

def wpa_check_activate(wpa_enabled, wpa_key):
	wpa_active = False
	reboot_required = False

	with open('/etc/hostapd/hostapd.conf') as hostapd_conf:
		for line in hostapd_conf:
			if 'wpa_passphrase' in line:
				wpa_active = True

	if wpa_enabled == '1' and wpa_active == False:
		reboot_required = True
		os.system('cp /usr/lib/raspiwifi/reset_device/static_files/hostapd.conf.wpa /etc/hostapd/hostapd.conf')

	if wpa_enabled == '1':
		with fileinput.FileInput('/etc/hostapd/hostapd.conf', inplace=True) as hostapd_conf:
			for line in hostapd_conf:
				if 'wpa_passphrase' in line:
					if 'wpa_passphrase=' + wpa_key not in line:
						print('wpa_passphrase=' + wpa_key)
						os.system('reboot')
					else:
						print(line, end = '')
				else:
					print(line, end = '')

	if wpa_enabled == '0' and wpa_active == True:
		reboot_required = True
		os.system('cp /usr/lib/raspiwifi/reset_device/static_files/hostapd.conf.nowpa /etc/hostapd/hostapd.conf')

	return reboot_required

def update_ssid(ssid_prefix, serial_last_four):
	reboot_required = False
	ssid_correct = False

	with open('/etc/hostapd/hostapd.conf') as hostapd_conf:
		for line in hostapd_conf:
			if ssid_prefix in line:
				ssid_correct = True

	if ssid_correct == False:
		with fileinput.FileInput("/etc/hostapd/hostapd.conf", inplace=True) as file:
			for line in file:
				if 'ssid=' in line:
					line_array = line.split('=')
					line_array[1] = ssid_prefix + ' ' + serial_last_four
					print(line_array[0] + '=' + line_array[1])
				else:
					print(line, end = '')

		reboot_required = True
			
	return reboot_required

def is_wifi_active():
	iwconfig_out = subprocess.check_output(['iwconfig']).decode('utf-8')
	wifi_active = True

	if "Access Point: Not-Associated" in iwconfig_out:
		wifi_active = False

	return wifi_active

def reset_to_host_mode():
	if not os.path.isfile('/etc/raspiwifi/host_mode'):
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
		os.system('touch /etc/raspiwifi/host_mode')
	os.system('reboot')
