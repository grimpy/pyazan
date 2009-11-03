import pynotify
import glib
from praytime import *
from location import *
from stopwatch import Alarm, isInSameDay
import datetime

loc = Location(name="Belguim", longitude=3.72, latitude=51.053, timezone=2)
loc2 = Location(name="Cairo", longitude=31.25, latitude=30.05, timezone=2)
praytimes = ['fajr','sunrise', 'duhr', 'asr', 'maghrib', 'isha']
pray_int = Praytime(loc2)

pynotify.init('pyazan')
nt = pynotify.Notification("Praying Time")

def getTomorrow():
    now = datetime.datetime.now()
    return now + datetime.timedelta(1)


def _getNexPrayer(prayer):
    nextprayeridx = praytimes.index(prayer)+1
    if nextprayeridx > len(praytimes)-1:
        nextprayeridx = 0
    return praytimes[nextprayeridx]

def _getPreviousPrayer(prayer):
    prevprayerindex = praytimes.index(prayer)-1
    if prevprayerindex < 0:
        prevprayerindex = len(praytimes) -1
    return praytimes[prevprayerindex]

def getNextPrayer(pray_int, prayer=None):
    nextprayer = None
    print prayer
    now = datetime.datetime.now()
    if prayer:
        nextprayer = _getNexPrayer(prayer)
        prayertime = getattr(pray_int, nextprayer)
        if isInSameDay(prayertime, now):
            return nextprayer, prayertime
        pray_int.day = getTomorrow()
        prayertime = getattr(pray_int, nextprayer)
        return nextprayer, prayertime
    else:
        for praytime in praytimes:
            prt = getattr(pray_int, praytime)
            if isInSameDay(prt, now):
                return praytime, prt
        pray_int.day = getTomorrow()
        prayertime = getattr(pray_int, praytimes[0])
        return praytimes[0], prayertime

def showNotify(message):
    nt.update(message)
    nt.set_timeout(0)
    nt.show()

prayername, prayertime = getNextPrayer(pray_int)
alarm = Alarm()

class PrayerTimes(object):
    def __init__(self, praytime):
        self.praytime = praytime
        self.waitingfor = getNextPrayer(self.praytime)
        prayername = _getPreviousPrayer(self.waitingfor[0])
        self.now = (prayername, getattr(self.praytime, prayername))
        self.waitingfor = self.now
    
    def showNotify(self, *args):
        showNotify("Time to pray %s" % (args[0][0]))
        self.now = self.waitingfor
    
    def main(self):
        if self.waitingfor == self.now:
            self.waitingfor = getNextPrayer(self.praytime, self.now[0])
            print self.waitingfor
            alarm.addAlarm(self.waitingfor[1], self.showNotify, self.waitingfor[0])
        return True
    
prt2 = PrayerTimes(pray_int)
glib.timeout_add_seconds(10, prt2.main)
glib.MainLoop().run()
