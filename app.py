from flask import Flask, render_template, request
import subprocess
import os
import time
from threading import Thread
from disable_access_point import disable_access_point
import fileinput

app = Flask(__name__)
app.debug = True


def set_wifi_credentials(ssid, password):
    try:
        config_lines = [
            "country=US",  # Replace 'US' with the appropriate country code for your region
            "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev",
            "update_config=1",
            "",
            "network={",
            f'\tssid="{ssid}"',
            "\tscan_ssid=1",
            f'\tpsk="{password}"',
            "\tkey_mgmt=WPA-PSK",
            "}",
        ]

        # Join the configuration lines into a single string
        config_data = "\n".join(config_lines)

        # Write the configuration to the wpa_supplicant file
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as wpafile:
            wpafile.write(config_data)

        t = Thread(target=disable_access_point)
        t.start()

        return True
    except Exception as e:
        print(e)
        return False


@app.route("/save_credentials", methods=["GET", "POST"])
def save_credentials():
    ssid = request.json["ssid"]
    wifi_key = request.json["wifi_key"]

    if set_wifi_credentials(ssid, wifi_key):
        return {"status": "success", "status_code": 200}
    else:
        return {"status": "failed", "status_code": 500}


@app.route("/connected", methods=["GET", "POST"])
def conncected():
    response = {"status_code": 200}
    return response


def run_api():
    app.run(host="0.0.0.0", port=5000)
