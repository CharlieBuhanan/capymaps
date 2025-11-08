import time
import datetime

class Capy:
    job:str
    timeOut:datetime
    startTime:datetime
    user:str # create user type when ready
    name:str
    coords = [-1,-1] # initial state
    building:str = "None"

    def __init__(self, timeOut:datetime, startTime:datetime, user:str, name:str, building:str="None", job:str="None"):
        self.job = job
        self.timeOut = timeOut
        self.startTime = startTime
        self.user = user
        self.name = name
        self.building = building
        return self

    def setCoords(self, x:int, y:int):
        self.coords = [x,y]
    def setJob(self, job:str):
        self.job = job
    def setName(self, name:str):
        self.name = name
    def setUser(self, user:str):
        self.user = user
    def setBuilding(self, building:str):
        self.building = building
    def setStartTime(self, startTime:datetime):
        self.startTime = startTime
    
    def getCoords(self):
        return self.coords
    def getJob(self):
        return self.job
    def getName(self):
        return self.name   
    def getBuilding(self):
        return self.building
    def getUser(self):  
        return self.user 
    def getStartTime(self):
        return self.startTime
    def getTimeOut(self):
        return self.timeOut
    def getElapsedTime(self):
        return datetime.datetime.now() - self.startTime

    def getTimeLeft(self): # not that useful for us, probably
        now = datetime.datetime.now()
        return self.timeOut - now

    def placeCapy(self, x=coords[0], y=coords[1]):
        # placeholder for future implementation. Place Capy on map at coords x,y
        self.setCoords(x,y)
        pass

    def removeCapy(self):
        # placeholder for future implementation. Remove Capy from Mmap
        self.setCoords(-1,-1)
        pass


