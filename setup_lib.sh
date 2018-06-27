#!/bin/sh

install_prereqs() {
  apt-get update
  apt-get install -y python3 python3-pip python3-rpi.gpio dnsmasq hostapd
  pip3 install -I 'Flask>=1.0.0'
}

copy_config() {
  mkdir /usr/lib/raspiwifi
  mkdir /etc/raspiwifi
  cp -a libs/* /usr/lib/raspiwifi/
  rm -f /etc/wpa_supplicant/wpa_supplicant.conf
  rm -rf ./tmp
  mv /etc/dnsmasq.conf /etc/dnsmasq.conf.original
  cp /usr/lib/raspiwifi/reset_device/static_files/dnsmasq.conf /etc/
  cp /usr/lib/raspiwifi/reset_device/static_files/hostapd.conf /etc/hostapd/
  mv /etc/dhcpcd.conf /etc/dhcpcd.conf.original
  cp /usr/lib/raspiwifi/reset_device/static_files/dhcpcd.conf /etc/
  mkdir /etc/cron.raspiwifi
  cp /usr/lib/raspiwifi/reset_device/static_files/aphost_bootstrapper /etc/cron.raspiwifi
  chmod +x /etc/cron.raspiwifi/aphost_bootstrapper
  echo "# RaspiWiFi Startup" >> /etc/crontab
  echo "@reboot root run-parts /etc/cron.raspiwifi/" >> /etc/crontab
  mv /usr/lib/raspiwifi/reset_device/static_files/raspiwifi.conf /etc/raspiwifi
}

update_config() {
  sed -i "s/RaspiWiFi Setup/${CONFIG_SSID:-RaspiWiFi Setup}/" /etc/raspiwifi/raspiwifi.conf
  [ "x$AUTO_CONFIG" = "xy" ] && sed -i "s/auto_config=0/auto_config=1/" /etc/raspiwifi/raspiwifi.conf
  sed -i "s/auto_config_delay=300/auto_config_delay=${AUTO_CONFIG_DELAY:-300}/" /etc/raspiwifi/raspiwifi.conf
}
