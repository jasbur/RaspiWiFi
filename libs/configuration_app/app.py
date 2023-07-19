from flask import Flask, render_template, request
import subprocess
import os
import time
from threading import Thread
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
            "\tkey_mgmt=1",
            "}",
        ]

        # Join the configuration lines into a single string
        config_data = "\n".join(config_lines)

        # Write the configuration to the wpa_supplicant file
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a") as wpafile:
            wpafile.write(config_data)

        t = Thread(target=os.system, args=("reboot",))
        t.start()

        return True
    except Exception as e:
        print(e)
        return False


@app.route("/save_credentials", methods=["GET", "POST"])
def save_credentials():
    ssid = request.form["ssid"]
    wifi_key = request.form["wifi_key"]

    if set_wifi_credentials(ssid, wifi_key):
        return {"status": "success", "status_code": 200}
    else:
        return {"status": "failed", "status_code": 500}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
