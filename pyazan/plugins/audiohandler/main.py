import gst, os, logging
from pyazan.paths import SOUND, XML
from pyazan.plugins import plugin

class Plugin(plugin.Plugin):
    def __init__(self):
        self.name = "audiohandler"
        self.file = None
        self.builder = None

    def play(self, *args):
        logging.info("Play")
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
        return self.pyazangui.options.getOption(self.name, "file", os.path.join(SOUND, "azan.mp3"))

    def getVolume(self):
        return int(self.pyazangui.options.getOption(self.name, "volume", 100))/100.0

    def save(self):
        volume = int(self.builder.get_object("volume").get_value())
        self.volume = volume/100.0
        self.pyazangui.options.setValue(self.name, "volume", volume)
        self.file = self.builder.get_object("file").get_filename()
        self.pyazangui.options.setValue(self.name, "file", self.file)

    def unload(self):
        self.pyazangui.praynotifier.onTime.removeCallback(self.play)

    def getUiWidget(self):
        widget = super(Plugin, self).getUiWidget()
        self.builder.get_object("file").set_filename(self.getAzanFile())
        self.builder.get_object("volume").set_value(self.getVolume()*100)
        self.builder.get_object("btn_test").connect("released", self.play)
        return widget

    def getDescription(self):
        return "Play Athan sound!"
