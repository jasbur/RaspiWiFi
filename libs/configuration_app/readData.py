import json
import os
from datetime import datetime
from operator import itemgetter


class currentTime():    # function that provides the current name day, date, and time
    nameDay = 0
    date = 0
    timeStamp = 0

    def time(self):
        currentTime.nameDay = datetime.now()
        currentTime.nameDay = currentTime.nameDay.strftime("%A")
        currentTime.nameDay = currentTime.nameDay[:3]
        currentTime.date = str(datetime.now())
        currentTime.timeStamp = currentTime.date.split(".")
        currentTime.timeStamp = currentTime.timeStamp[0].split(" ")
        currentTime.date = currentTime.timeStamp[0]
        currentTime.timeStamp = currentTime.timeStamp[1]

class jsonData():
    checkDay = []   # contains all the week data
    day2Check = []  # contains the data from an specific day 
    cycleStart = [] # contains the time for the cycle to start in HH:MM:SS
    cycleDuration = []  # time that will going to hold the 'on' task

    testStatus = False 
    testDuration = '0'
    fullPath = "/home/pi/feedtimer/server/device_config/device_config.json" # path file to read/write

    def cleanDataList(self):    # clean the lists for new incoming data
        del jsonData.checkDay[:]
        del jsonData.day2Check[:]
        del jsonData.cycleStart[:]
        del jsonData.cycleDuration[:]
        
    def saveData(self, d):  # save data for comparison 
        for i in d:
            jsonData.cycleStart.append(i["start"])  # set each input into the start list 
            jsonData.cycleDuration.append(i["duration"]) # set each input into the duration list
        print "day {} \nstart {} \nand duration {}, \n".format(jsonData.day2Check, jsonData.cycleStart, jsonData.cycleDuration)

    def checkTest(self, data):
        data = data["test"]
        if data["status"] == True or data["status"] == "true":
            jsonData.testStatus = True
            jsonData.testDuration = data["duration"]
        else:
            jsonData.testStatus = False
            
    def jsonData(self): # function to read, parse and sort the json file
        
        if not os.path.exists(jsonData.fullPath):    # if a json file not exists
            print("no json file")
        else:   # if a json file exists
            with open(jsonData.fullPath) as jsonFile:    # open the json fie
                data = json.load(jsonFile)  # save json string into 'data' variable
                self.checkTest(data)        # check for enabled tests in json file
                sortedData = dict(data)
                sortedData['days_of_week'] = sorted(data['days_of_week'], key=lambda x : x['cycles'], reverse=False)
                for day in data['days_of_week']:
                    for cycle in day['cycles']:     # iterate through each cycle 
                        status = cycle['status']
                        if type(status) == bool:    # if the status is boolean
                            if status == False:     # if the status object is false
                                pass
                            else:
                                currentTime().time()    # read the current time
                                if currentTime().nameDay == str(day['day']):    # if the current day matches with one day of the available cycles
                                    jsonData.day2Check.append(str(day['day']))
                                    jsonData.checkDay.append(cycle)
                                    
                        else:
                            if isinstance(status, unicode) == True: # if the status value is unicode 
                                if status == 'true':    # if the status is 'true'  
                                    currentTime().time()    # read the current time
                                    if currentTime().nameDay == str(day['day']):
                                        jsonData.day2Check.append(str(day['day']))
                                        jsonData.checkDay.append(cycle)
            
            if len(jsonData.checkDay) > 0:  # if the list is greater than 0
                jsonData.checkDay = sorted(jsonData.checkDay, key=itemgetter('start'))  # sort the list by 'start'
                for i in jsonData.checkDay: # iterate through each element to convert from unicode to str
                    i["duration"] = i.pop('duration')
                    i["duration"] = str(i["duration"])
                    i["start"] = i.pop('start')
                    i["start"] = str(i["start"])
                self.saveData(jsonData.checkDay)    # save data into lists for analysis
                print("starts {} \nduration {}".format(jsonData.cycleStart, jsonData.cycleDuration))
            else:   # there's no plan for today
                currentTime().time()    # read current day
                print "no plans for {}".format(currentTime().nameDay)
    
    def writeJson(data):
        if not os.path.exists(jsonData.fullPath):    # if a json file not exists
            print("no json file")
        else:   # if a json file exists
            jsonData.testStatus = False 
            with open(jsonData.fullPath, "r+") as jsonFile:
                data = json.load(jsonFile)
                test = data["test"]
                test["status"] = jsonData.testStatus   
                jsonFile.seek(0)    # rewind
                json.dump(data, jsonFile)
                jsonFile.truncate()

    def compareTimes(self, time1, time2):   # function to compare two time strings HH:MM:SS
        FMT = '%H:%M:%S'    # format for the output 
        return str(datetime.strptime(time2, FMT) - datetime.strptime(time1, FMT))
