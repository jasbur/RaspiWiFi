#!/bin/sh

set -e

cd "$(dirname "$0")"

cat <<'EOK'
###################################
##### RaspiWiFi Initial Setup #####
###################################
EOK
echo

# Ask for settings
read -p "Configuration mode SSID prefix [RaspiWiFi Setup]: " CONFIG_SSID
read -p "Enable auto-reconfiguration mode ? [y/N]: " AUTO_CONFIG
read -p "Auto-reconfiguration trigger delay (seconds) [300]: " AUTO_CONFIG_DELAY
read -p "Changes about to be committed to your Raspberry Pi. Continue? [y/N]: " GO_INSTALL

# Setup has been cancelled
if ! [ "x$GO_INSTALL" = "xy" ]; then
  echo
  cat <<'EOK'
RaspiWiFi installation was cancelled.
Nothing was changed. Exiting...
EOK
  exit 1
fi

# Do setup
. ./setup_lib.sh
install_prereqs
copy_config
update_config

echo
cat <<'EOK'
###################################
#### RaspiWiFi  Setup Complete ####
###################################
EOK
echo

# Ask for reboot
read -p "Reboot to start configuration mode [y/N]: " GO_REBOOT
if [ "x$GO_REBOOT" = "xy" ]; then
  reboot
fi
