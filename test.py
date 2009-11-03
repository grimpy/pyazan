import praytime
from location import Location

praytimes = ['fajr','sunrise', 'duhr', 'asr', 'maghrib', 'isha']
class Praytime(object):
    starttime = (0,20)
    counter = 0
    def __init__(self, *args):
        print "Construct", args
        for prayer in praytimes:
            setattr(self, prayer, (self.starttime[0],self.starttime[1]+Praytime.counter))
            Praytime.counter+=1

    def setDate(self, *args):
        print "SetDate", args


loc = Location(name="Belguim", longitude=3.72, latitude=51.053, timezone=2)
loc2 = Location(name="Cairo", longitude=31.25, latitude=30.05, timezone=2)
pr = praytime.Praytime(loc2)
print 'Fajr', pr.fajr
print 'Sunrise', pr.sunrise
print 'Duhr', pr.duhr
print 'Asr', pr.asr
print 'Mahrib', pr.maghrib
print 'Isha', pr.isha


