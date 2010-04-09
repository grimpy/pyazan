import logging, os
from pyazan.paths import XML

class Plugin(object):
    def __init__(self):
        self.name = None

    def load(self, *args):
        raise NotImplementedError

    def unload(self, *args):
        raise NotImplementedError

    def getDescription(self):
        return "No description"

    def getUiWidget(self):
        import gtk
        ui_config = os.path.join(XML, "%s.xml" % self.name)
        logging.info("Reading %s from ui", ui_config)
        if os.path.exists(ui_config):
            self.builder = gtk.Builder()
            self.builder.add_from_file(ui_config)
            return self.builder.get_object("plugin")
        return None

    def save(self):
        logging.warning("Save Not implemented %s",  self)
        pass
