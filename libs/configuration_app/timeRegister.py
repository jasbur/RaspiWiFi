import json 
from datetime import datetime

class Time_Register:
    '''
        Time register class 

        Read and write time saved
    '''
    def __init__(self, path):
        self.path = path 
        self.data = ''
        with open(self.path, 'r') as f:
            try: # if a valid json 
                self.data = json.load(f) # load json data
            except Exception:
                print("an invalid json is in the house")
                self.generateRegister()
    
    def isNewTimeGreater(self, newTime):
        newTime = datetime.strptime(newTime, '%Y-%m-%d %H:%M:%S')
        timeRegistered = datetime.strptime(self.data['system_time'], '%Y-%m-%d %H:%M:%S')
        return newTime > timeRegistered

    def readSystemTime(self):
        # get the system time
        # saved into a variable 
        today = datetime.now()
        rtcTime = today.strftime("%Y-%m-%d %H:%M:%S")
        return {"system_time":rtcTime}

    def getCurrentTime(self):
        today = datetime.now()
        currentTime = today.strftime("%Y-%m-%d %H:%M:%S")
        return currentTime

    def generateRegister(self):
        with open(self.path, "w") as jsonFile:
            json.dump(self.readSystemTime(), jsonFile)

    def read(self):
        return self.data["system_time"]

    def write(self, dateTime):
        with open(self.path, 'w') as jsonFile:
            self.data["system_time"] = dateTime # update data in json
            json.dump(self.data, jsonFile) # write data into json file

    def print_time(self):
        print(json.dumps(self.data, indent=4, sort_keys=True))

if __name__ == '__main__':
    path = 'time_register.json'
    t = Time_Register(path)
    new_time = '2021-07-31 17:55:22'

    comparison_result = t.isNewTimeGreater(new_time)
    if comparison_result:
        t.write(new_time)
        print(comparison_result)
        t.print_time()
    
