import pynotify
import datetime
import time
from praytime import *
from location import *
from threading import Timer
loc = Location(name="Belguim", longitude=3.72, latitude=51.053, timezone=2)
loc2 = Location(name="Cairo", longitude=31.25, latitude=30.05, timezone=2)
pr = Praytime(loc2)
pynotify.init('pyazan')
nt = pynotify.Notification("Praying Time")

def getTimeDiff(praytime):
    timenow = datetime.datetime.now()
    rpraytime = datetime.datetime(timenow.year, timenow.month, timenow.day , praytime[0], praytime[1])
    return rpraytime - timenow

def showNotify():
    nt.show()

dt = getTimeDiff(pr.isha)
t = Timer(5, showNotify)
t.start()
time.sleep(10)
