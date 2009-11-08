import gtk
import gobject
import pynotify
from praytime import PrayerTimesNotifier
from location import Location
from options import Options

class PyazanGTK(object):
    def __init__(self):
        self.mainloop = gobject.MainLoop()
        
        self.status_icon = gtk.StatusIcon()
        self.status_icon.set_from_file('azan.png')
        
        self.options = Options()
        
        self.build = gtk.Builder()
        self.build.add_from_file("pyazan_ui.xml")
        
        self.ui = dict(((x.get_name(), x) for x in self.build.get_objects() if hasattr(x, 'get_name')))
        self.attachSignals()
        
        pynotify.init('pyazan')
        self.notify = pynotify.Notification("Praying Time")
        
        self.loadOptions()
    
    def showNotify(self, prayer):
        self.notify.update("Time to pray '%s'" % prayer)
        self.notify.show()

    def loadOptions(self):
        praynotified = list()
        self.notify.set_timeout(self.options.getNotificationTimeout())
        praynotifies = self.options.getNotifications()
        location = self.options.getLocation()
        self.praynotifier = PrayerTimesNotifier(location, praynotifies)
        self.status_icon.set_tooltip("%s" % (self.praynotifier))
        
    
    def start(self):
        if self.options.isNotificationEnabled():
            self.praynotifier.onTime.addCallback(self.showNotify)
            self.praynotifier.start()
        self.mainloop.run()


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
