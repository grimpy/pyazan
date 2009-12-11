import gtk
import gobject
import os
from praytime import PrayerTimesNotifier, PRAYER_NAMES
from location import Location
from options import Options, getFullPath
from stopwatch import getTimeDiff

class PyazanGTK(object):
    def __init__(self):
        self.mainloop = gobject.MainLoop()
        
        self.status_icon = gtk.StatusIcon()
        self.status_icon.set_from_file(getFullPath('../data/mosque.png'))
        
        self.options = Options()
        
        self.build = gtk.Builder()
        self.build.add_from_file(getFullPath("../ui/pyazan_ui.xml"))
        
        self.ui = dict(((x.get_name(), x) for x in self.build.get_objects() if hasattr(x, 'get_name')))
        self.attachSignals()
        
        self.loadOptions()
        self.loadPlugins()
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
        location = self.options.getLocation()
        self.praynotifier = PrayerTimesNotifier(location, praynotifies)
        self.updateToolTip()

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
        #enable/disable notifications
        notification_enabled = self.ui["chkbtn_enablenot"].get_active()
        isenabled = self.praynotifier.onTime.hasCallback(self.showNotify)
        if isenabled and not notification_enabled:
            self.praynotifier.onTime.removeCallback(self.showNotify)
        elif not isenabled and notification_enabled:
            self.praynotifier.onTime.addCallback(self.showNotify)
        self.options.enableNotifications(notification_enabled)
        #set timeout
        notify_timeout = self.ui["spinbtn_not_timeout"].get_value_as_int()
        self.options.setNotificationTimeout(notify_timeout)
        self.notify.set_timeout(notify_timeout*1000)
        #text
        self.notifytext = self.ui["txt_nt"].get_text()
        self.options.setNotificationText(self.notifytext)
        
        self.options.save()
    
    def settingsOk(self, *args):
        self.applyConfig(*args)
        self.closeOptionsWindow(*args)
    
    def start(self):
        self.praynotifier.start()
        self.mainloop.run()

    def loadPlugins(self):
        self.plugins = dict((name, list()) for name in self.getPluginList())
        for plugin_name in self.plugins.keys():
            self.enablePlugin(plugin_name)

    def getPluginList(self):
        plugindir = getFullPath("plugins")
        for file in os.listdir(plugindir):
            if os.path.isdir(os.path.join(plugindir, file)):
                yield file

    def enablePlugin(self, plugin_name):
        if not self.plugins[plugin_name]:
            try:
                fromlist = [plugin_name]
                classes = getattr(__import__("pyazan.plugins", fromlist=fromlist), plugin_name)
                for klass in dir(classes):
                    import pdb; pdb.set_trace()
                    attrib = getattr(classes, klass)
                    if hasattr(attrib, "mro"):
                        self.plugins[plugin_name].append(attrib()) 
            except Exception, e:
                print "Failed to import plugin %s: %s" % (plugin_name, e)
                return False
        try:
            for pl in self.plugins[plugin_name]:
                print pl
                pl.load(self)
            return True
        except Exception, e:
            print "Failed to load plugin %s: %s" % (plugin_name, e)

    def disablePlugin(self, plugin_name):
        if self.plugins.get(plugin_name):
            for pl in self.plugins[plugin_name]:
                pl.unload()


    def attachSignals(self):
        #connect events
        self.ui["menuitem_quit"].connect("activate", self.quit)
        self.ui["menuitem_options"].connect("activate", self.showOptionsWindow)
        self.ui["btn_pref_cancel"].connect("released", self.closeOptionsWindow)
        self.ui["btn_pref_apply"].connect("released", self.applyConfig)
        self.ui["btn_pref_ok"].connect("released", self.settingsOk)
        
        self.status_icon.connect("popup-menu", self.showStatusIconPopup)

    def quit(self, *args):
        self.mainloop.quit()

    def closeOptionsWindow(self, *args):
        self.ui["pref_window"].hide()

    def showOptionsWindow(self, *args):
        self.ui["pref_window"].show()

    def showStatusIconPopup(self, icon, button ,timeout):
        self.ui["traymenu"].popup(None, None, None, button, timeout)
