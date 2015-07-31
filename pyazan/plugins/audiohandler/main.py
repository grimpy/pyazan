import gst, os, logging
from pyazan.paths import SOUND
from pyazan.plugins import plugin

class Plugin(plugin.Plugin):
    def __init__(self, *args, **kwargs):
        super(Plugin, self).__init__(*args, **kwargs)
        self.name = "audiohandler"
        self.file = self.getAzanFile()
        self.volume = self.getVolume()

    def play(self, *args):
        logging.info("Play")
        self.player = gst.element_factory_make("playbin", "player")
        self.player.set_property('uri', "file://%s" % self.file)
        self.player.set_property("volume", self.volume)
        self.player.set_state(gst.STATE_PLAYING)

    def load(self):
        self.pyazan.praynotifier.onTime.addCallback(self.play)

    def getAzanFile(self):
        return self.pyazan.options.getOption(self.name, "file", os.path.join(SOUND, "azan.mp3"))

    def getVolume(self):
        return int(self.pyazan.options.getOption(self.name, "volume", 100))/100.0

    def save(self):
        volume = int(self.builder.get_object("volume").get_value())
        self.volume = volume/100.0
        self.pyazan.options.setValue(self.name, "volume", volume)
        self.file = self.builder.get_object("file").get_filename()
        self.pyazan.options.setValue(self.name, "file", self.file)

    def unload(self):
        self.pyazan.praynotifier.onTime.removeCallback(self.play)

    def getUiWidget(self):
        widget = super(Plugin, self).getUiWidget()
        self.builder.get_object("file").set_filename(self.getAzanFile())
        self.builder.get_object("volume").set_value(self.getVolume()*100)
        self.builder.get_object("btn_test").connect("released", self.play)
        return widget

    def getDescription(self):
        return "Play Azan sound!"
