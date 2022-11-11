import requests
from bs4 import BeautifulSoup
import re
import json



class Parse:
    def __init__(self, uri):
       
        
        self.uri = uri
        self.req = requests.get(self.uri).text
        self.soup = BeautifulSoup(self.req, 'html.parser')
        self.times = ["8:00", "8:30", "9:00", "9:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30"]
        self.timetable = {"timetable":[]}

    def day_in(self, data):
        days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        for i in days:
            if i in data:
                return True
        return False

    def getColspan(self, data):
        if "colspan" in str(data):
            #print(data)
            return int(re.search(r'colspan=\"(.*?)\"', str(data)).group(1))
        return 1


    def readTables(self):

        timeTracker = 0
        i = 0
        table_begun = False
        previos_colspan = 0

        day = ""
        sTime = ""
        eTime = ""
        subject = ""
        classType = ""
        roomNumber = ""

        for td in self.soup.find_all('td'):

            
            if self.day_in(td.text):
                day = td.text
                table_begun = True
                timeTracker = 0
                i=0

            elif table_begun:
                
                if day=="Fri" and timeTracker >= (len(self.times)-1):
                    break
                
                previos_colspan = self.getColspan(td)
                
                if len(td.text) == 1:  
                    timeTracker+=1
                else:

                    if i % 5 == 0:
                        sTime = self.times[timeTracker]
                        eTime = self.times[timeTracker + previos_colspan]
                        
                        timeTracker+=previos_colspan


                    elif i % 5 == 1:
                        subject = td.text

                    elif i % 5 == 2:
                        roomNumber = td.text

                    elif i % 5 == 3:
                        classType = td.text

                    elif i % 5 == 4:

                        self.timetable["timetable"].append({"day": day, "startTime":sTime, "endTime":eTime, "subject":subject, "type":classType, "room":roomNumber, "teacher":td.text})

                    i+=1

    def getData(self):
        json_formatted_str = json.dumps(self.timetable, indent=2)
        print(json_formatted_str)

    def returnData(self):
        return self.timetable

if __name__ == "__main__":
    x = Parse("http://timetable.lit.ie:8080/reporting/individual;student+set;id;m_itSd1A%0D%0A?t=student+set+individual&days=1-5&weeks=&periods=1-28&template=student+set+individual")
    x.readTables()
    x.getData()


