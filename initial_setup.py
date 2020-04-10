import os
import sys
import setup_lib


if os.getuid():
    sys.exit('You need root access to install!')

os.system('clear')
print()
print()
print("###################################")
print("##### SymphonistWiFi Config Intial Setup  #####")
print("###################################")
entered_ssid = "symphonistWiFi Config"
wpa_enabled_choice = "y"
wpa_entered_key = "symphonist"
auto_config_choice = "N"
auto_config_delay = "300"
server_port_choice = "80"
ssl_enabled_choice = "N"
os.system('clear')


setup_lib.install_prereqs()
setup_lib.copy_configs(wpa_enabled_choice)
setup_lib.update_main_config_file(entered_ssid, auto_config_choice, auto_config_delay, ssl_enabled_choice, server_port_choice, wpa_enabled_choice, wpa_entered_key)


os.system('clear')
print()
print()
print("#####################################")
print("##### SymphonistWiFi Setup Complete  #####")
print("#####################################")
print()
print()
print("Initial setup is complete. A reboot is required to start in WiFi configuration mode...")

os.system('reboot')
