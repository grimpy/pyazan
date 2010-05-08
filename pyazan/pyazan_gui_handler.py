import gtk
import gobject
import os, logging
from praytime import PrayerTimesNotifier, PRAYER_NAMES
from options import Options
from paths import XML, TRAYICON
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
        self.ui['pref_window'].set_icon_from_file(TRAYICON)
        self.attach_signals()

        self.load_options()
        self.plugin_handler = PluginGTK(self)
        gobject.timeout_add_seconds(60, self.update_tool_tip)


    def update_tool_tip(self):
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

    def load_options(self):
        praynotifies = self.options.getNotifications()
        self.location = self.options.getLocation()
        self.praynotifier = PrayerTimesNotifier(self.location, praynotifies)
        self.update_tool_tip()

        self.ui["txt_location"].set_text(str(self.location))

        #set notify times in preference menu
        for prayer_name in PRAYER_NAMES:
            enabled = prayer_name in praynotifies
            self.ui["chkbnt_%s" % prayer_name].set_active(enabled)

    def apply_config(self, *args):
        #set prayer events
        pray_names_to_notify = list()
        for prayer_name in PRAYER_NAMES:
            if self.ui["chkbnt_%s" % prayer_name].get_active():
                pray_names_to_notify.append(prayer_name)
        self.options.setNotifications(pray_names_to_notify)
        self.praynotifier.alert_on = pray_names_to_notify
        #set location
        self.praynotifier.praytime.location = self.location
        self.options.setLocation(self.location)

        self.plugin_handler.save()
        self.options.save()

    def settings_ok(self, *args):
        self.apply_config(*args)
        self.close_options_window(*args)

    def start(self):
        self.praynotifier.start()
        self.mainloop.run()

    def load_location(self, *args):
        from location_ui import Location_ui
        Location_ui(self)

    def attach_signals(self):
        #connect events
        self.ui["menuitem_quit"].connect("activate", self.quit)
        self.ui["menuitem_options"].connect("activate", self.show_options_window)
        self.ui["btn_pref_cancel"].connect("released", self.close_options_window)
        self.ui["btn_pref_apply"].connect("released", self.apply_config)
        self.ui["btn_pref_ok"].connect("released", self.settings_ok)
        self.ui["btn_change_loc"].connect("released", self.load_location)

        self.status_icon.connect("popup-menu", self.show_status_icon_popup)

    def quit(self, *args):
        self.mainloop.quit()

    def close_options_window(self, *args):
        self.ui["pref_window"].destroy()

    def show_options_window(self, *args):
        self.ui["pref_window"].show()
        self.plugin_handler.load_options_window()

    def show_status_icon_popup(self, icon, button ,timeout):
        self.ui["traymenu"].popup(None, None, None, button, timeout)
