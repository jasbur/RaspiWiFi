import doorSystem as door
import readData as get
from time import sleep

workWeek = get.jsonData()
currentTime = get.currentTime()

def checkCycle():
    matchTime = '0:00:00'   # time difference to have for feeding
    if len(workWeek.day2Check) > 0:
        if workWeek.day2Check[0] == currentTime.nameDay:
            #print("day to check is: {}".format(workWeek.day2Check[0]))
            for i in range(0, len(workWeek.cycleStart)):
                print "will check {}".format(workWeek.cycleStart[i])
                if workWeek.compareTimes(currentTime.timeStamp, workWeek.cycleStart[i]) == matchTime:
                    print("there's a match! {}".format(workWeek.compareTimes(currentTime.timeStamp, workWeek.cycleStart[i])))
                    door.feed(workWeek.cycleDuration[i])    # feed with the selected time
                else:
                    print("this is the difference: {}".format(workWeek.compareTimes(currentTime.timeStamp, workWeek.cycleStart[i])))

def ifTest():
    if workWeek.testStatus == True:
        door.feed(float(workWeek.testDuration))
        workWeek.writeJson()

while True:
    currentTime.time()  # read time data
    workWeek.jsonData() # read json file
    ifTest()            # if a test status is enabled, this function is executed
    checkCycle()    # check if cycles are completed this week to open the feeder 
    sleep(1)    
    workWeek.cleanDataList()    # clean the list for incoming data

