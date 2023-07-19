import os

os.system("systemctl disable dnsmasq")
os.system("systemctl disable hostapd")

os.system("cp /etc/dnsmasq.conf.copy /etc/dnsmasq.conf.conf")
os.system("cp /etc/dhcpcd.conf.copy /etc/dhcpcd.conf")

os.system("reboot")
