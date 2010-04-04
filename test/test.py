#from pyazan import praytime, location
import datetime
#Location = location.Location

PRAYER_NAMES = ['fajr','sunrise', 'duhr', 'asr', 'maghrib', 'isha']

praytimes = PRAYER_NAMES

class Praytime(object):
    BEGIN = datetime.datetime.now()
    DELTA = datetime.timedelta(minutes=1)

    def __init__(self, *args):
        print "Construct", args
        self.setPrayers()

    def setPrayers(self):
        cnt = 0
        for prayer in praytimes:
            ntime = Praytime.BEGIN + Praytime.DELTA
            ptime = (ntime.hour,ntime.minute)
            setattr(self, prayer, ptime)
            if cnt % 1 == 0:
                Praytime.DELTA+=datetime.timedelta(minutes=1)
            cnt+=1

    def setDate(self, *args):
        print "SetDate", args
        self.setPrayers()

    day = property(fset=setDate)

    def __str__(self):
        strrepr = list()
        for praytime in PRAYER_NAMES:
            timetuple = getattr(self,praytime)
            timestring = "%02d:%02d" % (timetuple[0], timetuple[1])
            strrepr.append("%-14s\t%s" % (praytime.capitalize(), timestring))
        return "\n".join(strrepr)

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


