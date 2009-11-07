import pynotify
import gobject
from praytime import PrayerTimesNotifier
from location import Location
import gtk


pynotify.init('pyazan')
nt = pynotify.Notification("Praying Time")
nt.set_timeout(0)

def showNotify(prayer):
    nt.update("Time to pray '%s'" % prayer)
    nt.show()

if __name__ == "__main__":
    #init notifier.
    location = Location(name="Cairo", longitude=31.25, latitude=30.05, timezone=2)
    notifier = PrayerTimesNotifier(location)
    notifier.onTime.addCallback(showNotify)
    notifier.start()
    
    #gui stuff
    status_icon = gtk.StatusIcon()
    status_icon.set_from_file('azan.png')
    status_icon.set_tooltip("%s" % (notifier))

    #start the main program loop.
    gobject.MainLoop().run()
