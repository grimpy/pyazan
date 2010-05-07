import urllib, urllib2
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
    def __init__(self, name=None, longitude=None, latitude=None, timezone=0):
        self.longitude = longitude
        self.latitude = latitude
        self.name = name
        self.timezone = timezone

def _get_url(search):
    return "http://maps.google.com/maps/geo?%s" % urllib.urlencode({"q":search, "output":"json"})

def search(location):
    urlo = urllib2.urlopen(_get_url(location))
    data = urlo.read()
    rawdata = json.loads(data)
    for place in rawdata["Placemark"]:
        long, lat = place["Point"]["coordinates"][:-1]
        info = Location(place["address"], long, lat, 'auto')
        yield info

if __name__ == '__main__':
    print list(search("Stekene"))
