import pynotify
import glib
from praytime import *
from location import *
from stopwatch import Alarm
import datetime
import gtk

loc = Location(name="Belguim", longitude=3.72, latitude=51.053, timezone=2)
loc2 = Location(name="Cairo", longitude=31.25, latitude=30.05, timezone=2)
pray_int = Praytime(loc2)

pynotify.init('pyazan')
nt = pynotify.Notification("Praying Time")
nt.set_timeout(0)

def getTomorrow():
    now = datetime.datetime.now()
    return now + datetime.timedelta(1)

def showNotify(message):
    nt.update(message)
    nt.show()

alarm = Alarm()
status_icon = gtk.StatusIcon()
status_icon.set_from_file('azan.png')
status_icon.set_tooltip("%s" % (pray_int))

class PrayerTimes(object):
    def __init__(self, praytime):
        self.praytime = praytime
        self.waitingfor = getNextPrayer(self.praytime)
        prayername = getPreviousPrayerName(self.waitingfor[0])
        self.now = (prayername, getattr(self.praytime, prayername))
        self.waitingfor = self.now
    
    def showNotify(self, *args):
        showNotify("Time to pray %s" % (args[0][0]))
        self.now = self.waitingfor
        self.main()
    
    def main(self):
        if self.waitingfor == self.now:
            self.waitingfor = getNextPrayer(self.praytime, self.now[0])
            print self.waitingfor
            alarm.addAlarm(self.waitingfor[1], self.showNotify, self.waitingfor[0])
        return True
    
prt2 = PrayerTimes(pray_int)
prt2.main()
glib.MainLoop().run()
