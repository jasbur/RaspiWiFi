import os
import subprocess


def put_in_ap_mode():
    os.system("apt update")
    os.system("apt upgrade -y")
    os.system("apt install hostapd -y")
    os.system("apt install dnsmasq -y")
    os.system("systemctl stop hostapd")
    os.system("systemctl stop dnsmasq")
    os.system("apt install python3-pip -y")
    os.system("pip3 install flask")

    serial_last_four = subprocess.check_output(["cat", "/proc/cpuinfo"])[-5:-1].decode(
        "utf-8"
    )

    with open("/etc/hostapd/hostapd.conf", "w") as file:
        lines = [
            "interface=wlan0",
            "driver=nl80211",
            f"ssid=Device {serial_last_four}",
            "hw_mode=g",
            "channel=6",
            "wmm_enabled=0",
            "macaddr_acl=0",
            "ignore_broadcast_ssid=0",
        ]
        file.write("\n".join(lines))

    os.system("systemctl unmask hostapd")
    os.system("systemctl enable hostapd")

    if not os.path.exists("/etc/dnsmasq.conf"):
        open("/etc/dnsmasq.conf", "w").close()

    if os.path.exists("/etc/dnsmasq.conf.copy"):
        os.system("sudo cp /etc/dnsmasq.conf.copy /etc/dnsmasq.conf")

    os.system("cp /etc/dnsmasq.conf /etc/dnsmasq.conf.copy")

    with open("/etc/dnsmasq.conf", "a") as file:
        lines = [
            "#RPiHotspot config - No Intenet",
            "interface=wlan0",
            "domain-needed",
            "bogus-priv",
            "dhcp-range=192.168.50.150,192.168.50.200,255.255.255.0,12h",
            "address=/setup.com/192.168.50.10",
        ]
        file.write("\n".join(lines))

    if os.path.exists("/etc/dhcpcd.conf.copy"):
        os.system("sudo cp /etc/dhcpcd.conf.copy /etc/dhcpcd.conf")

    if not os.path.exists("/etc/dhcpcd.conf"):
        open("/etc/dhcpcd.conf", "w").close()

    os.system("cp /etc/dhcpcd.conf /etc/dhcpcd.conf.copy")

    with open("/etc/dhcpcd.conf", "a") as file:
        lines = [
            "interface wlan0",
            "nohook wpa_supplicant",
            "static ip_address=192.168.50.10/24",
            "static routers=192.168.50.1",
        ]
        file.write("\n".join(lines))

    os.system("raspi-config nonint do_wifi_country US")
    os.system("rfkill unblock wifi")

    os.system("reboot")
