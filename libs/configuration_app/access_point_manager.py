import subprocess
import os
import time
import tempfile

# The access point manager handles the logic relating to starting and stopping
# the access point on this device. When the device first starts we put the
# interface into host AP mode and handle configuration updates. After a timeout
# the device is put into client mode and connects to another AP.


class AccessPointManager:
    def start_access_point(self):
        print(subprocess.run(["killall", "dnsmasq"]))
        print(subprocess.run(["killall", "hostapd"]))
        print(subprocess.run(["ifconfig", "wlan0", "down"]))

        self.dnsmasq = subprocess.Popen(["dnsmasq", "--interface=wlan0",
                                         "--address=/#/10.0.0.1", "--dhcp-range=10.0.0.10,10.0.0.15,12h"])

        file, name = tempfile.mkstemp()

        serial_last_four = subprocess.getoutput(
            "cat /proc/cpuinfo | grep Serial | awk '{print $3}'")[-4:]

        hostapd_config = open(name, 'w')
        hostapd_config.write(
            'interface=wlan0\ndriver=nl80211\nssid=plantos-' + serial_last_four + '\nchannel=1')
        hostapd_config.close()

        print("wrote hostapd config file {}".format(name))

        # Set a static ip address on the device.
        dhcpcd_config = open('/etc/dhcpcd.conf', 'w')
        dhcpcd_config.write(
            'interface wlan0\nstatic ip_address=10.0.0.1/24\nstatic domain_name_servers=10.0.0.1\n# temporarily disable wpa_supplicant\nnohook wpa_supplicant')
        dhcpcd_config.close()
        print(subprocess.run(["systemctl", "restart", "dhcpcd"]))

        self.hostapd = subprocess.Popen(["hostapd", "-d", name])

    def stop_access_point(self):
        # TODO: Delete the hostapd config file.
        self.hostapd.terminate()
        self.dnsmasq.terminate()

        # Remove the static ip address and re-enable wpa_supplicant.
        dhcpcd_config = open('/etc/dhcpcd.conf', 'w')
        dhcpcd_config.write('')
        dhcpcd_config.close()
        print(subprocess.run(["systemctl", "restart", "dhcpcd"]))

# time.sleep(90.0)
