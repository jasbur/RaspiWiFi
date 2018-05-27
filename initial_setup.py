import os
import sys
import setup_lib

os.system('clear')
print()
print()
print("###################################")
print("##### RaspiWiFi Intial Setup  #####")
print("###################################")
print()
print()
install_ans = input("Would you like run the initial RaspiWiFi setup (This can take up to 5 minutes)? (y/n): ")
os.system('clear')
print()
print()
entered_ssid = input("Would you like to specify an SSID you'd like to use for Host/Configuration mode? [default: RaspiWiFi Setup]: ")

if(install_ans == 'y'):
	setup_lib.install_prereqs()
	setup_lib.copy_configs()
	setup_lib.update_main_config_file(entered_ssid)
	setup_lib.post_install_procs()

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
	os.system('reboot')
