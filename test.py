import praytime
from location import Location
loc = Location(name="Belguim", longitude=3.72, latitude=51.053, timezone=2)
loc2 = Location(name="Cairo", longitude=31.25, latitude=30.05, timezone=2)
pr = praytime.Praytime(loc2)
print 'Fajr', pr.fajr
print 'Sunrise', pr.sunrise
print 'Duhr', pr.duhr
print 'Asr', pr.asr
print 'Mahrib', pr.maghrib
print 'Isha', pr.isha


