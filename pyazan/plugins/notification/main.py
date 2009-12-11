import pynotify
from pyazan.options import getFullPath
from pyazan.plugins import plugin
pynotify.init('pyazan')

class Plugin(plugin.Plugin):
    def __init__(self):
        self.notify = pynotify.Notification("Praying Time")

    def load(self, pyazangui):
        print "Loading Notify"
        self.pyazangui = pyazangui
        self.notifytext = self.pyazangui.options.getNotificationText()
        self.notify.set_timeout(self.pyazangui.options.getNotificationTimeout()*1000)
        self.pyazangui.praynotifier.onTime.addCallback(self.showNotify)

    def unload(self):
        self.pyazangui.praynotifier.onTime.addCallback(self.showNotify)

    def showNotify(self, prayer, time):
        print "Something went wrong"
        notificationtext = "%s <b>%s</b> %02d:%02d" % (self.notifytext, prayer.capitalize(), time[0], time[1])
        self.notify.update("Praying Time", notificationtext, getFullPath("../data/azan.png"))
        self.notify.show()
