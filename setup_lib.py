import os


def install_prereqs():
    os.system('clear')
    os.system('apt update')
    os.system('clear')
    os.system('apt install python3 python3-rpi.gpio python3-pip dnsmasq hostapd -y')
    os.system('clear')
    print("Installing Flask web server...")
    print()
    os.system('pip3 install flask pyopenssl click')
    os.system('clear')


def copy_configs():
    os.system('mkdir /usr/lib/raspiwifi')
    os.system('mkdir /etc/raspiwifi')
    os.system('cp -a libs/* /usr/lib/raspiwifi/')
    os.system(
        'mv /etc/wpa_supplicant/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf.original')
    os.system('rm -f ./tmp/*')
    os.system('mv /etc/dnsmasq.conf /etc/dnsmasq.conf.original')
    os.system('cp /usr/lib/raspiwifi/reset_device/static_files/dnsmasq.conf /etc/')

    os.system(
        'cp /usr/lib/raspiwifi/reset_device/static_files/hostapd.conf.nowpa /etc/hostapd/hostapd.conf')

    os.system('mv /etc/dhcpcd.conf /etc/dhcpcd.conf.original')
    os.system('cp /usr/lib/raspiwifi/reset_device/static_files/dhcpcd.conf /etc/')
    os.system(
        'cp /usr/lib/raspiwifi/reset_device/static_files/portal.service /etc/systemd/system/')

    os.system('systemctl enable portal.service')
    os.system('systemctl start portal.service')

    os.system(
        'mv /usr/lib/raspiwifi/reset_device/static_files/raspiwifi.conf /etc/raspiwifi')
