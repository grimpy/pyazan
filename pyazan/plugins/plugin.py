import logging, os
from pyazan.paths import XML

class Plugin(object):
    def __init__(self):
        self.name = None
        self._cache = dict()

    def load(self, *args):
        raise NotImplementedError

    def unload(self, *args):
        raise NotImplementedError

    def getDescription(self):
        return "No description"

    def _get_builder(self):
        if "builder" not in self._cache:
            import gtk
            ui_config = os.path.join(XML, "%s.xml" % self.name)
            logging.info("Reading %s from ui", ui_config)
            if os.path.exists(ui_config):
                builder = gtk.Builder()
                builder.add_from_file(ui_config)
                self._cache['builder'] = builder
            else:
                self._cache['builder'] = None
        return self._cache['builder']

    builder = property(fget=_get_builder)

    def getUiWidget(self):
        if self.builder:
            return self.builder.get_object("plugin")
        return None

    def save(self):
        logging.warning("Save Not implemented %s",  self)
        pass
