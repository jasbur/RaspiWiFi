import os
import sys
import setup_lib


if os.getuid():
    sys.exit('You need root access to install!')


os.system('clear')
print()
print()
print("###################################")
print("##### RaspiWiFi Intial Setup  #####")
print("###################################")
print()
print()
entered_ssid = input("Would you like to specify an SSID you'd like to use \nfor Host/Configuration mode? [default: RaspiWiFi Setup]: ")
print()
auto_config_choice = input("Would you like to enable \nauto-reconfiguration mode [y/N]?: ")
print()
auto_config_delay = input("How long of a delay would you like without an active connection \nbefore auto-reconfiguration triggers (seconds)? [default: 300]: ")
print()
server_port_choice = input("Which port would you like to use for the Configuration Page? [default: 80]: ")
print()
ssl_enabled_choice = input("Would you like to enable SSL during configuration mode \n(NOTICE: you will get a certificate ID error \nwhen connecting, but traffic will be encrypted) [y/N]?: ")
os.system('clear')
print()
print()
install_ans = input("Are you ready to commit changes to the system? [y/N]: ")

if(install_ans.lower() == 'y'):
	setup_lib.install_prereqs()
	setup_lib.copy_configs()
	setup_lib.update_main_config_file(entered_ssid, auto_config_choice, auto_config_delay, ssl_enabled_choice, server_port_choice)
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
reboot_ans = input("Would you like to do that now? [y/N]: ")

if reboot_ans.lower() == 'y':
	os.system('reboot')
