#!/bin/sh

set -e

cd "$(dirname "$0")"

# Detect dry_run
if [ "x$1" = "xtest" ]; then
  DRY_RUN=y
  echo 'Running dry run, nothing will be applied.'
fi

# Ensure running as root
if ! [ "x$DRY_RUN" = "xy" ] && [ "$(/usr/bin/id -u)" -ne 0 ]; then
    echo "This script needs to be ran as root."
    echo "Please run: sudo $0"
    exit 1
fi

print_header() {
  c=${2:-'#'}
  line=$(head -c ${#1} < /dev/zero | tr '\0' "$c")
  printf "\\n$c$c$c$line$c$c$c\\n$c$c $1 $c$c\\n$c$c$c$line$c$c$c\\n"
}

print_header 'RaspiWiFi Initial Setup'
echo

# Ask for settings
printf "Configuration mode SSID prefix [RaspiWiFi Setup]: "
read -r CONFIG_SSID
printf "Enable auto-reconfiguration mode ? [y/N]: "
read -r AUTO_CONFIG
printf "Auto-reconfiguration trigger delay (seconds) [300]: "
read -r AUTO_CONFIG_DELAY
printf "Changes about to be committed to your Raspberry Pi. Continue? [y/N]: "
read -r GO_INSTALL

CONFIG_SSID=${CONFIG_SSID:-RaspiWifi Setup}
AUTO_CONFIG=${AUTO_CONFIG:-n}
AUTO_CONFIG_DELAY=${AUTO_CONFIG_DELAY:-300}
GO_INSTALL=${GO_INSTALL:-n}

# Setup has been cancelled
if ! [ "x$GO_INSTALL" = "xy" ]; then
  echo
  echo 'RaspiWiFi installation was cancelled.'
  echo 'Nothing was changed. Exiting...'
  exit 1
fi

# Do setup
. ./setup_lib.sh
print_header 'Install dependencies' '='
install_prereqs
print_header 'Copy config files' '='
copy_config
print_header 'Set config values' '='
update_config

print_header 'RaspiWiFi Setup Complete'
echo

# Ask for reboot
printf "Reboot to start configuration mode [y/N]: "
read -r GO_REBOOT
if ! [ "x$DRY_RUN" = "xy" ] && [ "x$GO_REBOOT" = "xy" ]; then
  reboot
fi
