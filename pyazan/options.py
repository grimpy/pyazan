
from ConfigParser import ConfigParser
import paths
import os
from location import Location
from praytime import PRAYER_NAMES

class Options(object):
    def __init__(self):
        self.filename = paths.CONFIGPATH
        defaults = {"timeout":0, "events": ",".join(PRAYER_NAMES)}
        self.options = ConfigParser(defaults)
        self.options.read(self.filename)

    def setValue(self, section, option, value):
        if not self.options.has_section(section):
            self.options.add_section(section)
        self.options.set(section, option, str(value))

    def getNotifications(self):
        if self.options.has_section("notification"):
            return self.options.get("notification", "events").split(",")
        return PRAYER_NAMES

    def getEnabledPlugins(self):
        if self.options.has_section("main"):
            return [ x.strip() for x in self.options.get("main", "plugins").split(",") ]
        return list()

    def setEnabledPlugins(self, plugins):
        self.setValue("main", "plugins", ",".join(plugins))

    def enablePlugin(self, name):
        pl = set(self.getEnabledPlugins())
        pl.add(name)
        self.setEnabledPlugins(pl)

    def getLocation(self):
        if self.options.has_section("location"):
            long = self.options.getfloat("location", "long")
            lat = self.options.getfloat("location", "lat")
            timezone = self.getOption("location", "timezone", "auto")
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

    def setNotifications(self, events):
        self.setValue("notification", "events", ",".join(events))

    def save(self):
        fd = open(self.filename, "w")
        self.options.write(fd)
