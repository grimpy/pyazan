import gst, os
from pyazan.paths import SOUND
from pyazan.plugins import plugin

class Plugin(plugin.Plugin):
    def __init__(self):
        self.file = None
        self.builder = None

    def play(self, *args):
        print "Play"
        self.player = gst.element_factory_make("playbin", "player")
        self.player.set_property('uri', "file://%s" % self.file)
        self.player.set_property("volume", self.volume)
        self.player.set_state(gst.STATE_PLAYING)

    def load(self, pyazangui):
        self.pyazangui = pyazangui
        self.file = self.getAzanFile()
        self.volume = self.getVolume()
        self.pyazangui.praynotifier.onTime.addCallback(self.play)

    def getAzanFile(self):
        return self.pyazangui.options.getOption("audiohandler", "file", os.path.join(SOUND, "azan.mp3"))

    def getVolume(self):
        return int(self.pyazangui.options.getOption("audiohandler", "volume", 100))/100.0

    def save(self):
        volume = int(self.builder.get_object("volume").get_value())
        self.volume = volume/100.0
        self.pyazangui.options.setValue("audiohandler", "volume", volume)
        self.file = self.builder.get_object("file").get_filename()
        self.pyazangui.options.setValue("audiohandler", "file", self.file)

    def unload(self):
        self.pyazangui.praynotifier.onTime.removeCallback(self.play)

    def getUiWidget(self):
        import gtk
        ui_config = os.path.join(os.path.dirname(__file__), "options.xml")
        self.builder = gtk.Builder()
        self.builder.add_from_file(ui_config)
        self.builder.get_object("file").set_filename(self.getAzanFile())
        self.builder.get_object("volume").set_value(self.getVolume()*100)
        self.builder.get_object("btn_test").connect("released", self.play)
        return self.builder.get_object("plugin")

    def getDescription(self):
        return "Play Athan sound!"
