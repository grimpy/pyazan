import pynotify, logging
from pyazan.paths import ICON
from pyazan.plugins import plugin
pynotify.init('pyazan')

class Plugin(plugin.Plugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.name = "notification"
        self.notify = pynotify.Notification("Praying Time")

    def load(self, pyazangui):
        self.pyazangui = pyazangui
        self.notifytext = self.pyazangui.options.getOption(self.name, "text", "It's time to pray")
        self.timeout = int(self.pyazangui.options.getOption(self.name, "timeout", 0))
        self.notify.set_timeout(self.timeout*1000)
        self.pyazangui.praynotifier.onTime.addCallback(self.showNotify)

    def unload(self):
        self.pyazangui.praynotifier.onTime.removeCallback(self.showNotify)

    def showNotify(self, prayer, time):
        notificationtext = "%s <b>%s</b> %02d:%02d" % (self.notifytext, prayer.capitalize(), time[0], time[1])
        self.notify.update("Praying Time", notificationtext, ICON)
        self.notify.show()

    def getUiWidget(self):
        widget = super(Plugin, self).getUiWidget()
        self.builder.get_object("txtbx").set_text(self.notifytext)
        self.builder.get_object("timeout").set_value(self.timeout)
        return widget

    def getDescription(self):
        return "Show notifcation via libnotify"

    def save(self):
        text = self.builder.get_object("txtbx").get_text()
        self.pyazangui.options.setValue(self.name, "text", text)
        self.timeout = int(self.builder.get_object("timeout").get_value())
        self.notify.set_timeout(self.timeout*1000)
        self.pyazangui.options.setValue(self.name, "timeout", self.timeout)
