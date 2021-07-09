'''
Description: Library to handle the digital outputs for the feeder
Open the Feeder on Pin 27
Close the Feeder on Pin 22
'''

from gpiozero import LED
from time import sleep 
import os
import datetime 

openDoor = LED(27)  # PIN 27
closeDoor = LED(22) # PIN 22

def close(timeOff):
    closeDoor.on()      # close the feeder
    sleep(timeOff)      # hold for time selected
    closeDoor.off()     # don't close the feeder

def feed(time):
    time = float(time)  # time to hold the 'on' task
    openDoor.on()       # open the door
    closeDoor.off()     # don't close the door
    sleep(time)         # hold for time selected
    openDoor.off()      # don't open the door
    close(time)         # start close the feeder
    