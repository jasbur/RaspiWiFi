# Captive Portal Wifi Configuration

This application allows users to configure wifi credentials for headless
devices. On boot the device starts broadcasting an access point that users can
connect to. Once connected users are presented with a captive portal, on
Android, iOS and most modern operating systems this is presented to the user
without any further interaction. The user is then presented with a list of
nearby wifi access points and prompted to pick one and fill in the password for
it. After filling the details the device stops its host AP and connects in
client mode using the supplied credentials.

This is a heavily modified version of https://github.com/jasbur/RaspiWiFi and
as such the GPLv3 license is carried over to this work.

## Installation

Install python, and some system dependencies.

```bash
sudo apt install -y python3 python3-rpi.gpio python3-pip dnsmasq hostapd
```

```bash
python3 -m pip install flask pyopenssl click
```

```bash
cp portal.service /etc/systemd/system/
systemctl enable portal.service
systemctl start portal.service
```
