import math
import time, datetime
from angle import *

class Location(object):
    def __init__(self, name=None, longitude=None, latitude=None, timezone=0):
        self.longitude = longitude
        self.latitude = latitude
        self.name = name
        self.timezone = timezone

class Praytime(object):
    _location = None
    _day = None

    def __init__(self, location=None, day=datetime.datetime.now()):
        self.location = location
        self.day = day
    
    def setLocation(self, location):
        if location:
            self._location = location
            self.calculatetimes()

    def setDay(self, day):
        if day:
            self._day = day
            self.calculatetimes()
    
    location = property(fset=setLocation, fget=lambda s: s._location)
    day = property(fset=setDay, fget=lambda s: s._day)
    
    def calculatetimes(self):
        if not self.day or not self.location:
            return
        day2000 = datetime.datetime(2000, 1, 1)
        d = (self.day-day2000).days 
        g = fixangle(357.529 + 0.98560028* d);
        q = fixangle(280.459 + 0.98564736* d);
        L = fixangle(q + 1.915* dsin(g) + 0.020* dsin(2*g));

        R = 1.00014 - 0.01671* dcos(g) - 0.00014* dcos(2*g);
        e = 23.439 - 0.00000036* d;
        RA = datan2(dcos(e)* dsin(L), dcos(L))/ 15;
        RA = fixhour(RA)

        D = dasin(dsin(e)* dsin(L));  # declination of the Sun
        EqT = q/15 - RA;  # equation of time

        sunsetangle = 0.8333
        duhr = 12+self.location.timezone - self.location.longitude/15 - EqT
        Fajr = duhr - self.tfunc(D, self.location.latitude, 19.5)
        Isha = duhr + self.tfunc(D, self.location.latitude, 17.5)
        self.fajr = getHoursMin(Fajr)
        self.sunrise = getHoursMin(duhr - self.tfunc(D, self.location.latitude, sunsetangle))
        self.duhr = getHoursMin(duhr)
        self.maghrib = getHoursMin(duhr + self.tfunc(D, self.location.latitude, sunsetangle))
        self.isha = getHoursMin(Isha)




    def tfunc(self, D, lati, angle):
        Z = (1.0/15) * dacos((-dsin(angle)-dsin(D)*dsin(lati))/(dcos(lati)*dcos(D)))
        return Z



def fixhour(a):
    a = a - 24.0 * (math.floor(a / 24.0));
    a = a+24.0 if a < 0 else a;
    return a;


def getHoursMin(hourdec):
    hour = int(hourdec)
    min = math.ceil((hourdec - hour)*(100)/(10)*(6))
    return hour, min

