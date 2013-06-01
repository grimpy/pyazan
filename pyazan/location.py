import urllib, urllib2, time
import logging

AUTO_TIME_ZONE = "AUTO"
try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import warnings
        warnings.warn("Ussing dirty hack to load JSON please install simplejson")
        class fakeJson(object):
            def loads(self, str):
                return eval(str)
        json = fakeJson()

class Location(object):
    def __init__(self, name=None, longitude=None, latitude=None, timezone=AUTO_TIME_ZONE):
        self.longitude = longitude
        self.latitude = latitude
        self.name = name
        self.timezone = timezone

    def _set_time_zone(self, timezone):
        self.timezoneconfig = timezone
        if isinstance(timezone, int) or timezone.isdigit():
            self._timezone = int(timezone)
        else:
            offset = time.timezone if not time.localtime().tm_isdst else time.altzone
            self._timezone = int(offset/3600) * -1
            logging.info("Auto timezone %d", self.timezone)


    timezone = property(fget=lambda s: s._timezone, fset=_set_time_zone)
    
    def __str__(self):
        return "%s - %s, %s" % (self.name, self.longitude, self.latitude)

    __repr__ = __str__

def _get_url(search):
    return "http://maps.googleapis.com/maps/api/geocode/json?%s" % urllib.urlencode({"address":search, "sensor": "false"})

def search(location):
    url = _get_url(location)
    print url
    urlo = urllib2.urlopen(url)
    data = urlo.read()
    rawdata = json.loads(data)
    if rawdata["status"] != "OK":
        return
    for place in rawdata["results"]:
        location = place['geometry']['location']
        info = Location(place["formatted_address"], location['lng'], location['lat'], 'auto')
        yield info

if __name__ == '__main__':
    print list(search("Stekene"))
