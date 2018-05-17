import subprocess
import fileinput
import os
import sys


def install_prereqs():
	project_path = os.path.dirname(os.path.abspath(__file__))

	os.system('clear')
	os.system('apt update')
	os.system('clear')
	os.system('apt install python3 python3-rpi.gpio bundler nodejs libsqlite3-dev dnsmasq hostapd libxml2-dev libxslt-dev -y')
	os.system('clear')
	os.system('gem install nokogiri --no-document -v 1.6.6.2 -- --use-system-libraries')
	os.system('clear')
	os.system('bundle install --gemfile=' + project_path + '/Configuration\ App/Gemfile')
	os.system('clear')

def update_config_paths():
	project_path = os.path.dirname(os.path.abspath(__file__))

	os.system('sudo cp -a Reset\ Device/static_files/apclient_bootstrapper.template Reset\ Device/static_files/apclient_bootstrapper')
	os.system('sudo cp -a Reset\ Device/static_files/aphost_bootstrapper.template Reset\ Device/static_files/aphost_bootstrapper')
	os.system('sudo cp -a Reset\ Device/reset_lib.py.template Reset\ Device/reset_lib.py')

	with fileinput.FileInput("Reset Device/static_files/aphost_bootstrapper", inplace=True) as file:
		for line in file:
			print(line.replace("[[project_dir]]", project_path), end='')
		file.close

	with fileinput.FileInput("Reset Device/static_files/apclient_bootstrapper", inplace=True) as file:
		for line in file:
			print(line.replace("[[project_dir]]", project_path), end='')
		file.close

	with fileinput.FileInput("Reset Device/reset_lib.py", inplace=True) as file:
		for line in file:
			print(line.replace("[[project_dir]]", project_path), end='')
		file.close


#################################################################
#################################################################

os.system('clear')
print()
print()
print("###################################")
print("##### RaspiWiFi Intial Setup  #####")
print("###################################")
print()
print()
install_ans = input("Would you like run the initial RaspiWiFi setup (This can take up to 5 minutes)? (y/n): ")

if(install_ans == 'y'):
	install_prereqs()
	update_config_paths()

	os.system('sudo rm -f /etc/wpa_supplicant/wpa_supplicant.conf')
	os.system('rm -f ./tmp/*')
	os.system('sudo cp -a ./Reset\ Device/static_files/dnsmasq.conf /etc/')
	os.system('sudo cp -a ./Reset\ Device/static_files/hostapd.conf /etc/hostapd/')
	os.system('mkdir /etc/cron.raspiwifi')
	os.system('sudo cp -a ./Reset\ Device/static_files/aphost_bootstrapper /etc/cron.raspiwifi')
	os.system('echo "# RaspiWiFi Startup" >> /etc/crontab')
	os.system('echo "@reboot root run-parts /etc/cron.raspiwifi/" >> /etc/crontab')
else:
	print()
	print()
	print("===================================================")
	print("---------------------------------------------------")
	print()
	print("RaspiWiFi installation cancelled. Nothing changed...")
	print()
	print("---------------------------------------------------")
	print("===================================================")
	print()
	print()
	sys.exit()

os.system('clear')
print()
print()
print("#####################################")
print("##### RaspiWiFi Setup Complete  #####")
print("#####################################")
print()
print()
print("Initial setup is complete. A reboot is required to start in WiFi configuration mode...")
reboot_ans = input("Would you like to do that now? (y/n): ")

if reboot_ans == 'y':
	os.system('sudo reboot')
