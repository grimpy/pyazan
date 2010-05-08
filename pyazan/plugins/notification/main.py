import pynotify, logging
from pyazan.paths import ICON
from pyazan.plugins import plugin
pynotify.init('pyazan')

class Plugin(plugin.Plugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.name = "notification"
        self.notify = pynotify.Notification("Praying Time")
        self._timeout = None
        self._notify_text = None

    def _get_timeout(self):
        if not self._builder:
            return int(self.pyazangui.options.getOption(self.name, "timeout", 0))
        else:
            return int(self.builder.get_object("timeout").get_value())

    def _set_timeout(self, timeout):
        self._timeout = timeout
        self.notify.set_timeout(self._timeout*1000)

    def _get_notify_text(self):
        if not self._builder:
            return self.pyazangui.options.getOption(self.name, "text", "It's time to pray")
        else:
            return self.builder.get_object("txtbx").get_text()

    def _set_notify_text(self, text):
        self._notify_text = text

    timeout = property(fget=_get_timeout, fset=_set_timeout)
    notify_text = property(fget=_get_notify_text, fset=_set_notify_text)

    def load(self, pyazangui):
        self.pyazangui = pyazangui
        self.pyazangui.praynotifier.onTime.addCallback(self.showNotify)

    def unload(self):
        self.pyazangui.praynotifier.onTime.removeCallback(self.showNotify)

    def showNotify(self, prayer, time):
        notificationtext = "%s <b>%s</b> %02d:%02d" % (self.notify_text, prayer.capitalize(), time[0], time[1])
        self.notify.update("Praying Time", notificationtext, ICON)
        self.notify.show()

    def _test(self, *args):
        self.showNotify("Test", (0,0))

    def getUiWidget(self):
        txt = self.notify_text
        timeout = self.timeout
        widget = super(Plugin, self).getUiWidget()
        self.builder.get_object("txtbx").set_text(txt)
        self.builder.get_object("timeout").set_value(timeout)
        self.builder.get_object("btn_test").connect("released", self._test)
        return widget

    def getDescription(self):
        return "Show notifcation via libnotify"

    def get_settings(self):
        text = self.builder.get_object("txtbx").get_text()
        timeout = int(self.builder.get_object("timeout").get_value())
        return text, timeout

    def save(self):
        self.pyazangui.options.setValue(self.name, "text", self.notify_text)
        self.pyazangui.options.setValue(self.name, "timeout", self.timeout)
