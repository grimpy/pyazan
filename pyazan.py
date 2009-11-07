#!/usr/bin/env python
import pynotify
import gobject
from praytime import PrayerTimesNotifier
from location import Location
import gtk
from pyazan_gui_handler import PyazanGTK
from options import Options


pynotify.init('pyazan')
nt = pynotify.Notification("Praying Time")
#nt.set_timeout(0)

def showNotify(prayer):
    nt.update("Time to pray '%s'" % prayer)
    nt.show()

if __name__ == "__main__":
    mainloop = gobject.MainLoop()
    #check notifytimeout
    options = Options()
    praynotified = list()
    nt.set_timeout(options.getNotificationTimeout())
    praynotifies = options.getNotifications()
    #init notifier.
    location = Location(name="Cairo", longitude=31.25, latitude=30.05, timezone=2)
    notifier = PrayerTimesNotifier(location, praynotifies)
    notifier.onTime.addCallback(showNotify)
    if options.isNotificationEnabled():
        notifier.start()
    
    #gui stuff
    status_icon = gtk.StatusIcon()
    status_icon.set_from_file('azan.png')
    status_icon.set_tooltip("%s" % (notifier))

    #create main gtkapp
    gtkbuild = gtk.Builder()
    gtkbuild.add_from_file("pyazan_ui.xml")
    PyazanGTK(mainloop, status_icon, gtkbuild, options)

    #start the main program loop.
    mainloop.run()
