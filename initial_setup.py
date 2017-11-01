import subprocess
import fileinput
import os
import sys


def install_prereqs():
	project_path = os.path.dirname(os.path.abspath(__file__))
	
	print("Updating Apt...")
	os.system('apt update')
	print("Installing prerequisites via Apt...")
	os.system('apt install python3 bundler libsqlite3-dev isc-dhcp-server hostapd libxml2-dev libxslt-dev -y')
	print("Installing necessary Ruby Gems. This can take a few minutes...")
	os.system('gem install nokogiri --no-document -v 1.6.6.2 -- --use-system-libraries')
	os.system('bundle install --gemfile=' + project_path + '/Configuration\ App/Gemfile')

def update_config_paths():
	project_path = os.path.dirname(os.path.abspath(__file__))

	os.system('sudo cp -a Reset\ Device/static_files/rc.local.aphost.template Reset\ Device/static_files/rc.local.aphost')
	os.system('sudo cp -a Reset\ Device/static_files/rc.local.apclient.template Reset\ Device/static_files/rc.local.apclient')
	os.system('sudo cp -a Reset\ Device/reset.py.template Reset\ Device/reset.py')

	with fileinput.FileInput("Reset Device/static_files/rc.local.aphost", inplace=True) as file:
		for line in file:
			print(line.replace("[[project_dir]]", project_path), end='')
		file.close

	with fileinput.FileInput("Reset Device/static_files/rc.local.apclient", inplace=True) as file:
		for line in file:
			print(line.replace("[[project_dir]]", project_path), end='')
		file.close

	with fileinput.FileInput("Reset Device/reset.py", inplace=True) as file:
		for line in file:
			print(line.replace("[[project_dir]]", project_path), end='')
		file.close


#################################################################
#################################################################


print()
print("###################################")
print("##### RaspiWiFi Intial Setup  #####")
print("###################################")
print()
print()
install_prereqs_ans = input("Would you like to install prerequisite files (This can take up to 5 minutes)? (y/n): ")

if(install_prereqs_ans == 'y'):
	print()
	print("Updating system...")
	install_prereqs()
else:
	print()
	print()
	print("===================================================")
	print("---------------------------------------------------")
	print()
	print("No Prerequisites installed. Continuing to configuration file installation...")
	print()
	print("---------------------------------------------------")
	print("===================================================")
	print()
	print()
	
print()
print()
print()
print()
run_setup_ans = input("Would you like to run the initial setup for RaspiWiFi? (y/n): ")

if(run_setup_ans == 'y'):
	print("Updating config files and copying them...")
	update_config_paths()

	os.system('sudo rm -f /etc/wpa_supplicant/wpa_supplicant.conf')
	os.system('rm -f ./tmp/*')
	os.system('sudo cp -r ./Reset\ Device/static_files/dhcpd.conf /etc/dhcp/')
	os.system('sudo cp -r ./Reset\ Device/static_files/hostapd.conf /etc/hostapd/')
	os.system('sudo cp -r ./Reset\ Device/static_files/interfaces.aphost /etc/network/interfaces')
	os.system('sudo cp -r ./Reset\ Device/static_files/isc-dhcp-server.aphost /etc/default/isc-dhcp-server')
	os.system('sudo cp -r ./Reset\ Device/static_files/rc.local.aphost /etc/rc.local')
else:
	print()
	print()
	print("===================================================")
	print("---------------------------------------------------")
	print()
	print("RaspiWiFi initial setup cancelled. No changes made.")
	print()
	print("---------------------------------------------------")
	print("===================================================")
	print()
	print()
	sys.exit(0)

print()
print()
reboot_ans = input("Initial setup is complete. A reboot is required, would you like to do that now? (y/n): ")

if(run_setup_ans == 'y' and reboot_ans == 'y'):
	os.system('sudo reboot')
