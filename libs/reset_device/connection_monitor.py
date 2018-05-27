import time
import reset_lib

no_conn_counter = 0

while True:
    time.sleep(10)

    if reset_lib.is_wifi_active() == False:
        print("No Connection for " + str(no_conn_counter) + " seconds...")
        no_conn_counter = no_conn_counter + 10
    else:
        print("Connection is active...")
        no_conn_counter = 0

    if no_conn_counter >= 30:
        print("Restting from inactivity...")
