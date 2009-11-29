import gst

class AudioHandler:
    def __init__(self, file):
        self.file = file

    def play(self, *args):
        self.player = gst.element_factory_make("playbin", "player")
        self.player.set_property('uri', "file://%s" % self.file)
        self.player.set_state(gst.STATE_PLAYING)
