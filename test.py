import praytime
loc = praytime.Location(name="Belguim", longitude=3.72, latitude=51.053, timezone=2)
print loc
pr = praytime.Praytime(loc)
pr.duhr
