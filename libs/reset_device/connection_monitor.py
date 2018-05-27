import time
import reset_lib

no_conn_counter = 0

while True:
    time.sleep(1)
    
    if reset_lib.is_wifi_active() == False:
        no_conn_counter = no_conn_counter + 1
    else:
        no_conn_counter = 0

    if no_conn_counter >= 30:
        print("Restting from inactivity...")
