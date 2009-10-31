import pynotify
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


def getNextPrayer(pray_int, prayer=None):
    nextprayer = None
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
    nt.show()

prayername, prayertime = getNextPrayer(pray_int)
alarm = Alarm()

while True:
    print prayertime, prayername
    alarm.addAlarm(prayertime, showNotify, "Time to pray %s" % prayername)
    alarm.waitForAlarm(prayertime)
    #get next prayer
    prayername, prayertime = getNextPrayer(pray_int, prayername)
