class Location(object):
    def __init__(self, name=None, longitude=None, latitude=None, timezone=0):
        self.longitude = longitude
        self.latitude = latitude
        self.name = name
        self.timezone = timezone
