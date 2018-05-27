import time
import reset_lib

no_conn_counter = 0

while True:
    time.sleep(10)

    if reset_lib.is_wifi_active() == False:
        no_conn_counter = no_conn_counter + 10
    else:
        no_conn_counter = 0

    if no_conn_counter >= 30:
        reset_lib.reset_to_host_mode()
