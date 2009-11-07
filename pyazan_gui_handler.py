import gtk

class PyazanGTK(object):
    def __init__(self, mainloop, status_icon, build, options):
        self.mainloop = mainloop
        self.status_icon = status_icon
        self.build = build
        self.ui = dict(((x.get_name(), x) for x in self.build.get_objects() if hasattr(x, 'get_name')))
        self.options = options
        self.attachSignals()

    def attachSignals(self):
        #connect events
        self.ui["menuitem_quit"].connect("activate", self.quit)
        self.ui["menuitem_options"].connect("activate", self.showOptionsWindow)
        self.ui["btn_pref_cancel"].connect("released", self.closeOptionsWindow)

        #get common used widgets
        self.ui_pref_window = self.build.get_object("pref_window")
        self.ui_traymenu = self.build.get_object("traymenu")
        self.status_icon.connect("popup-menu", self.showStatusIconPopup)

    def quit(self, *args):
        self.mainloop.quit()

    def closeOptionsWindow(self, *args):
        self.ui["pref_window"].hide()

    def showOptionsWindow(self, *args):
        self.ui["pref_window"].show()

    def showStatusIconPopup(self, icon, button ,timeout):
        self.ui["traymenu"].popup(None, None, None, button, timeout)
