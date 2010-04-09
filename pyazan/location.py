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

class GoogleLocation(object):
    def __init__(self):
        pass

    def getUrl(self, search):
        return "http://maps.google.com/maps/geo?%s" % urllib.urlencode({"q":search, "output":"json"})

    def search(self, location):
        urlo = urllib2.urlopen(self.getUrl(location))
        data = urlo.read()
        return json.loads(data)

if __name__ == '__main__':
    print GoogleLocation().search("Cairo")
