import os
import sys

print()
print("###################################")
print("##### RaspiWiFi Intial Setup  #####")
print("###################################")
print()
print()
run_setup_ans = input("Would you like to run the initial setup for RaspiWiFi? (y/n): ")

if(run_setup_ans == 'y'):
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
	print("---------------------------------------------------")
	print("---------------------------------------------------")
	print("RaspiWiFi initial setup cancelled. No changes made.")
	sys.exit(0)

print()
print()
reboot_ans = input("Initial setup is complete. A reboot is required, would you like to do that now? (y/n): ")

if(run_setup_ans == 'y' and reboot_ans == 'y'):
	os.system('sudo reboot')
