#!/usr/bin/env python3

import argparse
import os
import sys
import setup_lib


if os.getuid():
    sys.exit('You need root access to install!')

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument(
    "--ssid",
    required=False,
    default="RPI",
    help="SSID for host mode")

arg_parser.add_argument(
    '--auto-config-timeout',
    required=False,
    default=0,
    type=int,
    help='Switch to host mode after N seconds')

arg_parser.add_argument(
    '--use-https',
    required=False,
    default=False,
    action='store_true',
    help='Use SSL for web configurator access')

arg_parser.add_argument(
    '--port',
    required=False,
    default=80,
    type=int,
    help='Port for web configurator')

arg_parser.add_argument(
    "--wpa-key",
    required=False,
    default="",
    help="WPA key if decided to use WPA authentication")

arguments = arg_parser.parse_args(sys.argv[1:])

os.chdir(os.path.dirname(os.path.realpath(__file__)))

setup_lib.install_prereqs()
setup_lib.copy_configs("y" if arguments.wpa_key else "n")
setup_lib.update_main_config_file(
    arguments.ssid,
    "y" if arguments.auto_config_timeout else "n",
    str(arguments.auto_config_timeout),
    "y" if arguments.use_https else "n",
    str(arguments.port),
    "y" if arguments.wpa_key else "n",
    arguments.wpa_key
)

