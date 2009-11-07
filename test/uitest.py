import gtk
import gobject

status_icon = gtk.StatusIcon()
status_icon.set_from_file('../azan.png')
mainloop = gobject.MainLoop()
build = gtk.Builder()
build.add_from_file("../pyazan_ui.xml")


def quit(*args):
    print args
    mainloop.quit()

def showOptions(*args):
    pref_window = build.get_object("pref_window")
    pref_window.show()

menu = build.get_object("traymenu")
menuquit = build.get_object("menuitem_quit")
menuquit.connect("activate", quit)
menuoptions = build.get_object("menuitem_options")
menuoptions.connect("activate", showOptions)

def showPopup(icon, button ,timeout):
    menu.popup(None, None, None, button, timeout)

status_icon.connect("popup-menu", showPopup)
mainloop.run()
