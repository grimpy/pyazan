import praytime
import datetime
from location import Location

praytimes = praytime.PRAYER_NAMES
NOW = datetime.datetime.now()
DELTA = datetime.timedelta(minutes=0)
NOW = NOW - DELTA
class Praytime(object):
    starttime = (NOW.hour,NOW.minute)
    counter = 0
    def __init__(self, *args):
        print "Construct", args
        for prayer in praytimes:
            setattr(self, prayer, (self.starttime[0],self.starttime[1]+Praytime.counter))
            Praytime.counter+=2

    def setDate(self, *args):
        print "SetDate", args
    
    def __str__(self):
        return "This is a test class"

if __name__ == '__main__':
    loc = Location(name="Belguim", longitude=3.72, latitude=51.053, timezone=2)
    loc2 = Location(name="Cairo", longitude=31.25, latitude=30.05, timezone=2)
    pr = praytime.Praytime(loc2)
    print 'Fajr', pr.fajr
    print 'Sunrise', pr.sunrise
    print 'Duhr', pr.duhr
    print 'Asr', pr.asr
    print 'Mahrib', pr.maghrib
    print 'Isha', pr.isha


