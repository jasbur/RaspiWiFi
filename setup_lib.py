import os

def install_prereqs():
	os.system('clear')
	os.system('apt update')
	os.system('clear')
	os.system('apt install python3 python3-rpi.gpio bundler nodejs libsqlite3-dev dnsmasq hostapd libxml2-dev libxslt-dev -y')
	os.system('clear')

def copy_configs():
	os.system('mkdir /usr/lib/raspiwifi')
	os.system('mkdir /etc/raspiwifi')
	os.system('cp -a libs/* /usr/lib/raspiwifi/')
	os.system('rm -f /etc/wpa_supplicant/wpa_supplicant.conf')
	os.system('rm -f ./tmp/*')
	os.system('mv /etc/dnsmasq.conf /etc/dnsmasq.conf.original')
	os.system('cp /usr/lib/raspiwifi/reset_device/static_files/dnsmasq.conf /etc/')
	os.system('cp /usr/lib/raspiwifi/reset_device/static_files/hostapd.conf /etc/hostapd/')
	os.system('mv /etc/dhcpcd.conf /etc/dhcpcd.conf.original')
	os.system('cp /usr/lib/raspiwifi/reset_device/static_files/dhcpcd.conf /etc/')
	os.system('mkdir /etc/cron.raspiwifi')
	os.system('cp /usr/lib/raspiwifi/reset_device/static_files/aphost_bootstrapper /etc/cron.raspiwifi')
	os.system('chmod +x /etc/cron.raspiwifi/aphost_bootstrapper')
	os.system('echo "# RaspiWiFi Startup" >> /etc/crontab')
	os.system('echo "@reboot root run-parts /etc/cron.raspiwifi/" >> /etc/crontab')
	os.system('mv /usr/lib/raspiwifi/reset_device/static_files/raspiwifi.conf /etc/raspiwifi')

def update_main_config_file(entered_ssid, auto_config_choice):
	if entered_ssid != "":
		os.system('sed -i \'s/RaspiWiFi Setup/' + entered_ssid + '/\' /etc/raspiwifi/raspiwifi.conf')
	if auto_config_choice.lower() == "y":
		os.system('sed -i \'s/auto_config=0/auto_config=1/\' /etc/raspiwifi/raspiwifi.conf')

def post_install_procs():
	os.system('gem install nokogiri --no-document -v 1.6.6.2 -- --use-system-libraries')
	os.system('clear')
	os.system('bundle install --gemfile=/usr/lib/raspiwifi/configuration_app/Gemfile')
	os.system('clear')
