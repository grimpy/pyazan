import pynotify, logging
from pyazan.paths import ICON
from pyazan.plugins import plugin
pynotify.init('pyazan')

class Plugin(plugin.Plugin):
    def __init__(self):
        self.notify = pynotify.Notification("Praying Time")

    def load(self, pyazangui):
        self.pyazangui = pyazangui
        self.notifytext = self.pyazangui.options.getNotificationText()
        self.notify.set_timeout(self.pyazangui.options.getNotificationTimeout()*1000)
        self.pyazangui.praynotifier.onTime.addCallback(self.showNotify)

    def unload(self):
        self.pyazangui.praynotifier.onTime.removeCallback(self.showNotify)

    def showNotify(self, prayer, time):
        notificationtext = "%s <b>%s</b> %02d:%02d" % (self.notifytext, prayer.capitalize(), time[0], time[1])
        self.notify.update("Praying Time", notificationtext, ICON)
        self.notify.show()

    def getDescription(self):
        return "Show notifcation via libnotify"
