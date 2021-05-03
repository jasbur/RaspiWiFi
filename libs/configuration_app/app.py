from werkzeug.serving import make_server
from flask import Flask, render_template, request, redirect
import subprocess
import os
import time
import threading
import fileinput
from access_point_manager import AccessPointManager


class ServerThread(threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.srv = make_server('0.0.0.0', 80, app, threaded=True)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        print('starting server')
        self.srv.serve_forever()

    def shutdown(self):
        print('shutting down server')
        self.srv.shutdown()


app = Flask(__name__)
app.debug = True

server = ServerThread(app)
manager = AccessPointManager()


@app.route('/portal')
def index():
    wifi_ap_array = scan_wifi_networks()
    config_hash = config_file_hash()

    return render_template('app.html', wifi_ap_array=wifi_ap_array, config_hash=config_hash)


@app.route('/manual_ssid_entry')
def manual_ssid_entry():
    return render_template('manual_ssid_entry.html')


@app.route('/wpa_settings')
def wpa_settings():
    config_hash = config_file_hash()
    return render_template('wpa_settings.html', wpa_enabled=config_hash['wpa_enabled'], wpa_key=config_hash['wpa_key'])


@app.route('/save_credentials', methods=['GET', 'POST'])
def save_credentials():
    ssid = request.form['ssid']
    wifi_key = request.form['wifi_key']

    create_wpa_supplicant(ssid, wifi_key)

    # Kill flask and proceed to start the AP in client mode.
    server.shutdown()

    return render_template('save_credentials.html', ssid=ssid)


@app.route('/save_wpa_credentials', methods=['GET', 'POST'])
def save_wpa_credentials():
    config_hash = config_file_hash()
    wpa_enabled = request.form.get('wpa_enabled')
    wpa_key = request.form['wpa_key']

    if str(wpa_enabled) == '1':
        update_wpa(1, wpa_key)
    else:
        update_wpa(0, wpa_key)

    # Kill flask and proceed to start the AP in client mode.
    server.shutdown()

    config_hash = config_file_hash()
    return render_template('save_wpa_credentials.html', wpa_enabled=config_hash['wpa_enabled'], wpa_key=config_hash['wpa_key'])


# On mobile devices, captive portal detection requires that HTTP requests to
# certain well-known urls return the correct status code. For example, on
# Android devices an HTTP request is sent to
# http://clients1.google.com/generate_204 and if the response is not status 204
# it is assumed to be a captive portal. We ensure this logic works correctly by
# returning an HTTP 302 that specifies the location of this web app.
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return redirect("http://10.0.0.1/portal")


######## FUNCTIONS ##########

def scan_wifi_networks():
    iwlist_raw = subprocess.Popen(
        ['iwlist', 'wlan0', 'scan'], stdout=subprocess.PIPE)
    ap_list, err = iwlist_raw.communicate()
    ap_array = []

    # The output of iwscan is a series of ascii bytes containing utf8 escape
    # characters. First parse the unicode escape sequences (\xAA) then decode
    # the utf8 contents.
    for line in ap_list.decode('unicode-escape').encode('latin1').decode('utf8').rsplit('\n'):
        if 'ESSID' in line:
            ap_ssid = line[27:-1]
            if ap_ssid != '':
                ap_array.append(ap_ssid)

    return ap_array


def create_wpa_supplicant(ssid, wifi_key):
    temp_conf_file = open('wpa_supplicant.conf.tmp', 'w')

    temp_conf_file.write(
        'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n')
    temp_conf_file.write('update_config=1\n')
    temp_conf_file.write('\n')
    temp_conf_file.write('network={\n')
    temp_conf_file.write('	ssid="' + ssid + '"\n')

    if wifi_key == '':
        temp_conf_file.write('	key_mgmt=NONE\n')
    else:
        temp_conf_file.write('	psk="' + wifi_key + '"\n')

    temp_conf_file.write('	}')

    temp_conf_file.close

    os.system('mv wpa_supplicant.conf.tmp /etc/wpa_supplicant/wpa_supplicant.conf')
    os.system('wpa_cli -i wlan0 reconfigure')

    print(subprocess.run(["killall", "dnsmasq"]))
    print(subprocess.run(["killall", "hostapd"]))

    # Remove the static ip address and re-enable wpa_supplicant.
    dhcpcd_config = open('/etc/dhcpcd.conf', 'w')
    dhcpcd_config.write('')
    dhcpcd_config.close()
    print(subprocess.run(["systemctl", "restart", "dhcpcd"]))


def update_wpa(wpa_enabled, wpa_key):
    with fileinput.FileInput('/etc/raspiwifi/raspiwifi.conf', inplace=True) as raspiwifi_conf:
        for line in raspiwifi_conf:
            if 'wpa_enabled=' in line:
                line_array = line.split('=')
                line_array[1] = wpa_enabled
                print(line_array[0] + '=' + str(line_array[1]))

            if 'wpa_key=' in line:
                line_array = line.split('=')
                line_array[1] = wpa_key
                print(line_array[0] + '=' + line_array[1])

            if 'wpa_enabled=' not in line and 'wpa_key=' not in line:
                print(line, end='')


def config_file_hash():
    config_file = open('/etc/raspiwifi/raspiwifi.conf')
    config_hash = {}

    for line in config_file:
        line_key = line.split("=")[0]
        line_value = line.split("=")[1].rstrip()
        config_hash[line_key] = line_value

    return config_hash


def stop_after_timeout():
    time.sleep(5 * 60)
    print("Timeout reached. Stopping server.")
    server.shutdown()


if __name__ == '__main__':
    config_hash = config_file_hash()

    # Stop the server after a timeout.
    thread = threading.Thread(target=stop_after_timeout, args=())
    thread.daemon = True                            # Daemonize thread
    thread.start()                                  # Start the execution

    print("starting access point in host mode")
    manager.start_access_point()
    print("starting flask")
    server.start()
    server.join()
    print("stopped flask")
    print("stopping host mode access point")
    manager.stop_access_point()
    print("stopped access point")
