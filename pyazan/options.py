from ConfigParser import ConfigParser
import os
from location import Location
from praytime import PRAYER_NAMES

def getFullPath(value):
    basepath = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(basepath, value)

class Options(object):
    def __init__(self):
        XDG_HOME = os.environ.get("XDG_CONFIG_HOME")
        if not XDG_HOME:
            XDG_HOME = os.path.expanduser(os.path.join("~", ".config"))
        self.filename = os.path.join(XDG_HOME, "pyazan.cfg")
        defaults = {"timeout":0, "events": ",".join(PRAYER_NAMES), "enabled": True, "text":"It's time to pray"}
        self.options = ConfigParser(defaults)
        self.options.read(self.filename)

    def setValue(self, section, option, value):
        if not self.options.has_section(section):
            self.options.add_section(section)
        self.options.set(section, option, value)

    def getNotifications(self):
        if self.options.has_section("notification"):
            return self.options.get("notification", "events").split(",")
        return PRAYER_NAMES

    def getNotificationTimeout(self):
        if self.options.has_section("notification"):
            return self.options.getint("notification", "timeout")
        return 0

    def getLocation(self):
        if self.options.has_section("location"):
            long = self.options.getfloat("location", "long")
            lat = self.options.getfloat("location", "lat")
            timezone = self.options.getint("location", "timezone")
            name = self.options.get("location", "name")
            return Location(name, long, lat, timezone)
        return None

    def getOption(self, section, value, default, boolean=False):
        if self.options.has_section(section):
            if boolean:
                return self.options.getboolean(section, value)
            else:
                return self.options.get(section, value)
        return default

    def setLocation(self, location):
        self.setValue("location", "name", location.name)
        self.setValue("location", "long", location.longitude)
        self.setValue("location", "lat", location.latitude)
        self.setValue("location", "timezone", location.timezone)

    def setNotificationTimeout(self, value):
        self.setValue("notification", "timeout", int(value))

    def setNotifications(self, events):
        self.setValue("notification", "events", ",".join(events))
    
    def getNotificationText(self):
        return self.getOption("notification", "text", "It's time to pray")
    
    def setNotificationText(self, text):
        self.setValue("notification", "text", text)

    def save(self):
        fd = open(self.filename, "w")
        self.options.write(fd)

    def enableNotifications(self, flag):
        self.setValue("notification", "enabled", flag)

    def isNotificationEnabled(self):
        return self.getOption("notification", "enabled", True, True)
