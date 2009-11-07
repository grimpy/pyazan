import gtk

class PyazanGTK(object):
    def __init__(self, mainloop, status_icon, build):
        self.mainloop = mainloop
        self.status_icon = status_icon
        self.build = build
        self.attachSignals()

    def attachSignals(self):
        #connect events
        menuquit = self.build.get_object("menuitem_quit")
        menuquit.connect("activate", self.quit)
        menuoptions = self.build.get_object("menuitem_options")
        menuoptions.connect("activate", self.showOptionsWindow)
        btn_pref_cancel = self.build.get_object("btn_pref_cancel")
        btn_pref_cancel.connect("released", self.closeOptionsWindow)

        #get common used widgets
        self.gui_pref_window = self.build.get_object("pref_window")
        self.gui_traymenu = self.build.get_object("traymenu")
        self.status_icon.connect("popup-menu", self.showStatusIconPopup)

    def quit(self, *args):
        self.mainloop.quit()

    def closeOptionsWindow(self, *args):
        self.gui_pref_window.hide()

    def showOptionsWindow(self, *args):
        self.gui_pref_window.show()

    def showStatusIconPopup(self, icon, button ,timeout):
        self.gui_traymenu.popup(None, None, None, button, timeout)
