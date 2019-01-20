import os
import sys

os.system('clear')
print()
print()
print("#################################")
print("##### RaspiWiFi Uninstaller #####")
print("#################################")
print()
print()
uninstall_answer = input("Would you like to uninstall RaspiWiFi? [y/N]: ")
print()

if (uninstall_answer.lower() == "y"):
    os.system('rm -rf /etc/raspiwifi')
    os.system('rm -rf /usr/lib/raspiwifi')
    os.system('rm -rf /etc/cron.raspiwifi')
    os.system('rm /etc/dnsmasq.conf')
    os.system('mv /etc/dnsmasq.conf.original /etc/dnsmasq.conf')
    os.system('rm /etc/hostapd/hostapd.conf')
    os.system('rm /etc/dhcpcd.conf')
    os.system('mv /etc/dhcpcd.conf.original /etc/dhcpcd.conf')
    os.system('sed -i \'s/# RaspiWiFi Startup//\' /etc/crontab')
    os.system('sed -i \'s/@reboot root run-parts \/etc\/cron.raspiwifi\///\' /etc/crontab')
else:
    print()
    print('No changes made. Exiting unistaller...')