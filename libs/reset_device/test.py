import reset_lib
import os

config_hash = reset_lib.config_file_hash()

if config_hash['wpa_enabled'] == '1':
    os.system('cp /usr/lib/raspiwifi/reset_device/static_files/hostapd.conf.wpa /etc/hoastapd/hostapd.conf')
    reset_lib.update_wpa_key(config_hash['wpa_key'])