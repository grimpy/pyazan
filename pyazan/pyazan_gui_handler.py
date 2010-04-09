import gtk
import gobject
import os, logging
from praytime import PrayerTimesNotifier, PRAYER_NAMES
from location import Location
from options import Options
from paths import *
from stopwatch import getTimeDiff

class UiDict(dict):
    def __init__(self, builder):
        self.builder = builder
        self.cache = dict()

    def __getitem__(self, name):
        if name not in self.cache:
            self.cache[name] = self.builder.get_object(name)
        return self.cache[name]

class PyazanGTK(object):
    def __init__(self):
        self.mainloop = gobject.MainLoop()

        self.status_icon = gtk.StatusIcon()
        self.status_icon.set_from_file(TRAYICON)

        self.options = Options()

        self.build = gtk.Builder()
        self.build.add_from_file(os.path.join(XML, 'pyazan_ui.xml'))

        self.ui = UiDict(self.build)
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

    def loadPlugins(self):
        self.plugins = dict((name, list()) for name in self.getPluginList())
        for plugin_name in self.plugins.keys():
            if plugin_name in self.options.getEnabledPlugins():
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
                    attrib = getattr(classes, klass)
                    if hasattr(attrib, "mro"):
                        self.plugins[plugin_name] = attrib()
            except Exception, e:
                logging.error("Failed to import plugin %s: %s", plugin_name, e)
                return False
        try:
            self.plugins[plugin_name].load(self)
            logging.info("Loaded %s", plugin_name)
            return True
        except Exception, e:
            logging.error("Failed to load plugin %s: %s", plugin_name, e)

    def disablePlugin(self, plugin_name):
        if self.plugins.get(plugin_name):
            self.plugins[plugin_name].unload()


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

    def pluginChanged(self, cell, position, model):
        iter = model.get_iter((int(position),))
        value = not cell.get_active()
        if iter:
            plugin_name = model.get_value(iter, 1)
            if value:
                self.enablePlugin(plugin_name)
            else:
                self.disablePlugin(plugin_name)
        model.set_value(iter, 0, value)

    def getSelectedPlugin(self):
        treeview = self.ui['plugin_tree']
        selector = treeview.get_selection()
        model, iter = selector.get_selected()
        plugin_name = model.get_value(iter, 1)
        enabled = model.get_value(iter, 0)
        return plugin_name, enabled

    def selectPlugin(self, treeview, event):
        plugin_name, enabled = self.getSelectedPlugin()
        if plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]
            self.ui["lbl_plugin_name"].set_text(plugin_name.capitalize())
            self.ui["plugin_description"].set_text(plugin.getDescription())
            widget = plugin.getUiWidget()
            plc_hld = self.ui["plugin_pref_placeholder"]
            for child in plc_hld.get_children():
                plc_hld.remove(child)
            if not widget:
                self.ui["btn_plugin_preferences"].set_sensitive(False)
            else:
                self.ui["btn_plugin_preferences"].set_sensitive(True)
                widget.show()
                plc_hld.add(widget)


    def showOptionsWindow(self, *args):
        self.ui["pref_window"].show()
        model = self.ui["plugin_tree"].get_model()
        self.ui["plugin_tree"].connect("button-release-event", self.selectPlugin)
        # column for enable/disable
        renderer = gtk.CellRendererToggle()
        renderer.connect('toggled', self.pluginChanged, model)
        column = gtk.TreeViewColumn('Enabled', renderer, active=0)
        # set this column to a fixed sizing(of 50 pixels)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_fixed_width(50)
        self.ui["plugin_tree"].append_column(column)
        #append name collum
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('Name', renderer, text=1)
        self.ui["plugin_tree"].append_column(column)
        for k, v in self.plugins.iteritems():
            iter = model.append()
            enabled = k in self.options.getEnabledPlugins()
            model.set(iter, 0, enabled, 1, k)

    def showStatusIconPopup(self, icon, button ,timeout):
        self.ui["traymenu"].popup(None, None, None, button, timeout)
