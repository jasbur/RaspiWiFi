import time
import sys
import os
import reset_lib

no_conn_counter = 0
consecutive_active_reports = 0
config_hash = reset_lib.config_file_hash()

if config_hash['auto_config'] == "0":
    sys.exit()
else:
    while True:
        time.sleep(10)

        if reset_lib.is_wifi_active() == False:
            no_conn_counter += 10
            consecutive_active_reports = 0
            os.system('echo no conn counter: ' + str(no_conn_counter) + ' seconds >> /home/pi/connlog')
        else:
            consecutive_active_reports += 1
            no_conn_counter += 10
            os.system('echo consecutive_active_reports: ' + str(consecutive_active_reports) + ' >> /home/pi/connlog')
            if consecutive_active_reports >= 2:
                no_conn_counter = 0

        if no_conn_counter >= int(config_hash['auto_config_delay']):
            reset_lib.reset_to_host_mode()
