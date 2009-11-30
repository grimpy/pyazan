import gst
from pyazan.options import getFullPath

class Plugin:
    def __init__(self):
        self.file = None

    def play(self, *args):
        self.player = gst.element_factory_make("playbin", "player")
        self.player.set_property('uri', "file://%s" % self.file)
        self.player.set_state(gst.STATE_PLAYING)

    def load(self, pyazangui):
        self.pyazangui = pyazangui
        self.file = self.getAzanFile()
        self.pyazangui.praynotifier.onTime.addCallback(self.play)

    def getAzanFile(self):
        return self.pyazangui.options.getOption("sound", "file", getFullPath("azan.mp3"))

    def unload():
        self.pyazangui.praynotifier.onTime.removeCallback(self.play)

