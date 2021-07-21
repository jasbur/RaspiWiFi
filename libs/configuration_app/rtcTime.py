import subprocess
from datetime import datetime
from time import time
from timeRegister import Time_Register

min_tries = 0
max_tries = 5

time_register = Time_Register('time_register.json')

def read(): # read the time on the RTC module 
    try:
        limitTimeArray = 19 # amount of characters to read on the string 
        rtcTime = subprocess.check_output("sudo hwclock -r", shell = True)  # read the output of the rtc clock reading 
        rtcTime = rtcTime[:limitTimeArray]  # save the target time 
        return rtcTime      # return time saved
    except subprocess.CalledProcessError:   # if an error happens
        today = datetime.now()
        rtcTime = today.strftime("%Y-%m-%d %H:%M:%S")
        return rtcTime      # return time saved

def setSystClock(time): # set the system clock 
    timeGoal = str("sudo date -s " + '"' + time + '"')  # set string to input systemclock with time as parameter
    RtcTimeGoal = str("sudo hwclock -w")  # write time into RTC module
    subprocess.call(timeGoal, shell = True)             # call process to set the systemclock time 
    subprocess.call(RtcTimeGoal, shell = True)             # call process to set the systemclock time 

timeRead = read() # get the current time from rtc or system 
setSystClock(timeRead)    # set the systems clock
    