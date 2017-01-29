puts
puts "###################################"
puts "##### RaspiWiFi Initial Setup #####"
puts "###################################"
puts
puts
print "Would you like to run the initial setup for RaspiWiFi? (y/n): "
run_setup_ans = gets.chomp.downcase

if run_setup_ans == 'y'
	system('sudo rm -f /etc/wpa_supplicant/wpa_supplicant.conf')
	system('rm -f ./tmp/*')
	system('sudo cp -r ./Reset\ Device/static_files/dhcpd.conf /etc/dhcp/')
	system('sudo cp -r ./Reset\ Device/static_files/hostapd.conf /etc/hostapd/')
	system('sudo cp -r ./Reset\ Device/static_files/interfaces.aphost /etc/network/interfaces')
	system('sudo cp -r ./Reset\ Device/static_files/isc-dhcp-server.aphost /etc/default/isc-dhcp-server')
	system('sudo cp -r ./Reset\ Device/static_files/rc.local.aphost /etc/rc.local')
else
	puts
	puts
	puts "---------------------------------------------------"
	puts "---------------------------------------------------"
	abort("RaspiWiFi initial setup cancelled. No changes made.")
end

puts
puts
print "Initial setup is complete. A reboot is required, would you like to do that now? (y/n): "
reboot_ans = gets.chomp.downcase

if run_setup_ans == 'y' and reboot_ans == 'y'
	system('sudo reboot')
end
