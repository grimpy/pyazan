import gst
from pyazan.options import getFullPath

class AudioHandler:
    def __init__(self, file):
        self.file = file

    def play(self, *args):
        self.player = gst.element_factory_make("playbin", "player")
        self.player.set_property('uri', "file://%s" % self.file)
        self.player.set_state(gst.STATE_PLAYING)


audio = AudioHandler(getFullPath('azan.mp3'))
pyazangui = None

def load(pyazangui):
    pyazangui.praynotifier.onTime.addCallback(audio.play)

def unload():
    pyazangui.praynotifier.onTime.removeCallback(audio)

def getAzanFile(self):
    return self.getOption("sound", "file", getFullPath("azan.mp3"))
