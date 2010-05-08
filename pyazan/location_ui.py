import gtk, gobject

import location
from ui_common import UiDict
from paths import XML
import os, logging

class Location_ui(object):
    def __init__(self, pyazan_ui):
        self.pyazan_ui = pyazan_ui
        self.ui = UiDict(os.path.join(XML, 'location.xml'))
        self.model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_FLOAT, gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT)
        self.ui["tree_loc"].set_model(self.model)
        self.load()

    def load(self):
        self.ui["wnd_loc_search"].show()
        self.ui["txtbx_loc_search"].connect("activate", self.search)
        self.ui["btn_loc_search"].connect("released", self.search)
        self.ui["btn_loc_ok"].connect("released", self.ok_clicked)
        self.ui["btn_loc_can"].connect("released", self.cancel_clicked)

    def close_window(self, *args):
        self.ui["wnd_loc_search"].destroy()

    def search(self, *args):
        logging.info("Location search pressed")
        model = self.ui["tree_loc"].get_model()
        for loc in location.search(self.ui["txtbx_loc_search"].get_text()):
            iter = model.append()
            model.set(iter, 0, loc.name, 1, loc.longitude, 2, loc.latitude, 3, loc)
            logging.debug(str(loc))

    def ok_clicked(self, *args):
        logging.info("Location ok pressed")
        location = self.get_selection()
        if location:
            self.pyazan_ui.ui["txt_location"].set_text(str(location))
            self.pyazan_ui.location = location
        self.close_window()

    def cancel_clicked(self, *args):
        logging.info("Location cancel pressed")
        self.close_window()

    def get_selection(self):
        treeview = self.ui['tree_loc']
        selector = treeview.get_selection()
        model, iter = selector.get_selected()
        if not iter:
            return
        return model.get_value(iter, 3)
