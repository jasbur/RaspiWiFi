import os
import sys
import setup_lib


if os.getuid():
    sys.exit('You need root access to install!')


setup_lib.install_prereqs()
setup_lib.copy_configs()

print()
print()
print("#####################################")
print("##### RaspiWiFi Setup Complete  #####")
print("#####################################")
print()
print()
print("Initial setup is complete. A reboot is required to start in WiFi configuration mode...")
reboot_ans = input("Would you like to do that now? [y/N]: ")

if reboot_ans.lower() == 'y':
    os.system('reboot')
