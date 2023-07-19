import os

os.system("apt update")
os.system("apt upgrade -y")
os.system("apt install hostapd -y")
os.system("apt install dnsmasq -y")
os.system("systemctl stop hostapd")
os.system("systemctl stop dnsmasq")
os.system("apt install python3-pip -y")
os.system("pip3 install flask")

with open("/etc/hostapd/hostapd.conf", "w") as file:
    lines = [
        "interface=wlan0"
        "driver=nl80211"
        "ssid=Ballbert"
        "hw_mode=g"
        "channel=6"
        "wmm_enabled=0"
        "macaddr_acl=0"
        "auth_algs=1"
        "ignore_broadcast_ssid=0"
        "wpa=2"
        "wpa_passphrase=Ballbert"
        "wpa_key_mgmt=WPA-PSK"
        "rsn_pairwise=CCMP"
    ]
    file.write("\n".join(lines))

os.system("systemctl unmask hostapd")
os.system("systemctl enable hostapd")

os.system("cp /etc/dnsmasq.conf /etc/dnsmasq.conf.copy")

with open("/etc/dnsmasq.conf", "a") as file:
    lines = [
        "#RPiHotspot config - No Intenet",
        "interface=wlan0",
        "domain-needed",
        "bogus-priv",
        "dhcp-range=192.168.50.150,192.168.50.200,255.255.255.0,12h",
        "address=/setup.ballbert.com/10.0.0.1",
    ]
    file.write("\n".join(lines))

os.system("cp /etc/dhcpcd.conf /etc/dhcpcd.conf.copy")

with open("/etc/dhcpcd.conf", "a") as file:
    lines = [
        "interface wlan0",
        "nohook wpa_supplicant",
        "static ip_address=192.168.50.10/24",
        "static routers=192.168.50.1",
    ]
    file.write("\n".join(lines))

os.system("rfkill unblock wifi")

os.system("reboot")
