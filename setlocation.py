from location import Location
from options import Options
opt = Options()
loc2 = Location(name="Cairo", longitude=31.25, latitude=30.05, timezone=2)
opt.setLocation(loc2)
opt.save()
