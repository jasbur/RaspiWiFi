import time
import sys
import reset_lib

no_conn_counter = 0
config_hash = reset_lib.config_file_hash()

if config_hash['auto_config'] == 0:
    sys.exit()
else:
    while True:
        time.sleep(10)

        if reset_lib.is_wifi_active() == False:
            no_conn_counter = no_conn_counter + 10
        else:
            no_conn_counter = 0

        if no_conn_counter >= int(config_hash['auto_config_delay']):
            reset_lib.reset_to_host_mode()
