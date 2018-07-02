#!/bin/sh

set -e

cd "$(dirname "$0")"

# Ensure running as root
if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "This script needs to be ran as root."
    echo "Please run: sudo $0"
    exit 1
fi

# Detect dry_run
if [ "x$1" = "xtest" ]; then
  DRY_RUN=y
  echo 'Running dry run, nothing will be applied.'
fi

print_header() {
  c=${2:-'#'}
  line=$(head -c ${#1} < /dev/zero | tr '\0' $c)
  printf "\n$c$c$c$line$c$c$c\n$c$c $1 $c$c\n$c$c$c$line$c$c$c\n"
}

print_header 'RaspiWiFi Initial Setup'

# Ask for settings
read -p "Configuration mode SSID prefix [RaspiWiFi Setup]: " CONFIG_SSID
read -p "Enable auto-reconfiguration mode ? [y/N]: " AUTO_CONFIG
read -p "Auto-reconfiguration trigger delay (seconds) [300]: " AUTO_CONFIG_DELAY
read -p "Changes about to be committed to your Raspberry Pi. Continue? [y/N]: " GO_INSTALL

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

# Ask for reboot
read -p "Reboot to start configuration mode [y/N]: " GO_REBOOT
if [ "x$GO_REBOOT" = "xy" ]; then
  reboot
fi
