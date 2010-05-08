import gtk
import gobject
import os, logging
from praytime import PrayerTimesNotifier, PRAYER_NAMES
from location import Location
from options import Options
from paths import *
from stopwatch import getTimeDiff
from ui_common import UiDict
from plugin_gui_handler import PluginGTK

class PyazanGTK(object):
    def __init__(self):
        self.mainloop = gobject.MainLoop()

        self.status_icon = gtk.StatusIcon()
        self.status_icon.set_from_file(TRAYICON)

        self.options = Options()

        self.ui = UiDict(os.path.join(XML, 'pyazan_ui.xml'))
        self.attachSignals()

        self.loadOptions()
        self.plugin_handler = PluginGTK(self)
        gobject.timeout_add_seconds(60, self.updateToolTip)


    def updateToolTip(self):
        prayer, time = self.praynotifier.now
        tooltiplist = str(self.praynotifier).split("\n")
        currentindex = PRAYER_NAMES.index(prayer)+2
        if len(tooltiplist) > currentindex:
            tooltiplist[currentindex] = "<u>%s</u>" % tooltiplist[currentindex]
        nicetime = str(getTimeDiff(self.praynotifier.waitingfor[1])).split(":")[0:2]
        tooltiplist.append("\nTime until next prayer %s" % ":".join(nicetime))
        if hasattr(self.status_icon.props, 'tooltip_markup'):
            self.status_icon.props.tooltip_markup = "\n".join(tooltiplist)
        else:
            self.status_icon.set_tooltip("\n".join(tooltiplist))
        return True

    def loadOptions(self):
        praynotified = list()
        praynotifies = self.options.getNotifications()
        self.location = self.options.getLocation()
        self.praynotifier = PrayerTimesNotifier(self.location, praynotifies)
        self.updateToolTip()

        self.ui["txt_location"].set_text(str(self.location))

        #set notify times in preference menu
        for prayer_name in PRAYER_NAMES:
            enabled = prayer_name in praynotifies
            self.ui["chkbnt_%s" % prayer_name].set_active(enabled)

    def applyConfig(self, *args):
        #set prayer events
        pray_names_to_notify = list()
        for prayer_name in PRAYER_NAMES:
            if self.ui["chkbnt_%s" % prayer_name].get_active():
                pray_names_to_notify.append(prayer_name)
        self.options.setNotifications(pray_names_to_notify)
        self.praynotifier.alert_on = pray_names_to_notify
        #save enabled plugins
        index = 0
        enabled_plugins = list()
        model = self.ui["liststore_plugins"]
        for index in xrange(model.iter_n_children(None)):
            iter = model.iter_nth_child(None, index)
            plugin_name = model.get_value(iter, 1)
            enabled = model.get_value(iter, 0)
            if enabled:
                enabled_plugins.append(plugin_name)
        self.options.setEnabledPlugins(enabled_plugins)
        for pl in self.plugins.itervalues():
            pl.save()
        self.options.save()

    def settingsOk(self, *args):
        self.applyConfig(*args)
        self.closeOptionsWindow(*args)

    def start(self):
        self.praynotifier.start()
        self.mainloop.run()

    def load_location(self, *args):
        from location_ui import Location_ui
        Location_ui(self)

    def attachSignals(self):
        #connect events
        self.ui["menuitem_quit"].connect("activate", self.quit)
        self.ui["menuitem_options"].connect("activate", self.showOptionsWindow)
        self.ui["btn_pref_cancel"].connect("released", self.closeOptionsWindow)
        self.ui["btn_pref_apply"].connect("released", self.applyConfig)
        self.ui["btn_pref_ok"].connect("released", self.settingsOk)
        self.ui["btn_change_loc"].connect("released", self.load_location)

        self.status_icon.connect("popup-menu", self.showStatusIconPopup)

    def quit(self, *args):
        self.mainloop.quit()

    def closeOptionsWindow(self, *args):
        self.ui["pref_window"].destroy()

    def showOptionsWindow(self, *args):
        self.ui["pref_window"].show()
        self.plugin_handler.load_options_window()

    def showStatusIconPopup(self, icon, button ,timeout):
        self.ui["traymenu"].popup(None, None, None, button, timeout)
