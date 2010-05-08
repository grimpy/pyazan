import logging
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

from pyazan.plugins import plugin

class Plugin(plugin.Plugin):
    def __init__(self, *args, **kwargs):
        super(Plugin, self).__init__(*args, **kwargs)
        self.name = "dbus"
        self.dbus = None

    def load(self):
        self.dbus = PyAzanDbus()
        self.pyazan.praynotifier.onTime.addCallback(self.send_signal)

    def unload(self):
        self.pyazan.praynotifier.onTime.removeCallback(self.send_signal)

    def send_signal(self, prayer, time):
        self.dbus.praytime(prayer, time[0], time[1])

    def getUiWidget(self):
        widget = super(Plugin, self).getUiWidget()
        return widget

    def getDescription(self):
        return "Expose pyazan events over dbus"

class PyAzanDbus(dbus.service.Object):
    def __init__(self):
        dbus_loop = DBusGMainLoop()
        bus = dbus.SessionBus(mainloop=dbus_loop)
        bus_name = dbus.service.BusName('com.github.grimpy.pyazan', bus=bus)
        dbus.service.Object.__init__(self, bus_name, '/com/github/grimpy/pyazan')
        self.prayerinfo = None

    @dbus.service.signal(dbus_interface='com.github.grimpy.pyazan', signature='sii')
    def praytime(self, prayer, hour, time):
        self.prayerinof = args
