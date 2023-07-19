import os


def uninstall():
    os.system("systemctl disable dnsmasq")
    os.system("systemctl disableg hostapd")

    os.system("cp /etc/dnsmasq.conf.copy /etc/dnsmasq.conf.conf")
    os.system("cp /etc/dhcpcd.conf.copy /etc/dhcpcd.conf")

    os.system("reboot")


if __name__ == "__main__":
    uninstall()
    print("Uninstalling...")
