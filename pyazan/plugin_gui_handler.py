import os, logging
import gtk

from paths import getFullPath

class PluginLoader(dict):
    def __init__(self, pyazan):
        self._pyazan = pyazan
        self._cache = dict()

    def __getitem__(self, name):
        if name not in self._cache:
            try:
                fromlist = [name]
                classes = getattr(__import__("pyazan.plugins", fromlist=fromlist), name)
                for klass in dir(classes):
                    attrib = getattr(classes, klass)
                    if hasattr(attrib, "mro"):
                        self._cache[name] = attrib(self._pyazan)
            except Exception, e:
                logging.error("Failed to import plugin %s: %s", name, e)
                return False
        return self._cache[name]

    def __iter__(self):
        for x in self._cache:
            yield x


class PluginGTK(object):
    def __init__(self, pyazan):
        self.ui = pyazan.ui
        self.pyazan = pyazan
        self.plugins = PluginLoader(pyazan)
        self.load_plugins()

    def load_plugins(self):
        for plugin_name in self.get_plugin_list():
            if plugin_name in self.pyazan.options.getEnabledPlugins():
                self.enable_plugin(plugin_name)

    def get_plugin_list(self):
        plugindir = getFullPath("plugins")
        for file in os.listdir(plugindir):
            if os.path.isdir(os.path.join(plugindir, file)):
                yield file

    def enable_plugin(self, plugin_name):
        try:
            if self.plugins[plugin_name]:
                self.plugins[plugin_name].load()
                logging.info("Loaded %s", plugin_name)
                return True
        except Exception, e:
            logging.error("Failed to load plugin %s: %s", plugin_name, e)

    def disable_plugin(self, plugin_name):
        if self.plugins.get(plugin_name):
            self.plugins[plugin_name].unload()

    def plugin_changed(self, cell, position, model):
        iter = model.get_iter((int(position),))
        value = not cell.get_active()
        if iter:
            plugin_name = model.get_value(iter, 2)
            if value:
                self.enable_plugin(plugin_name)
            else:
                self.disable_plugin(plugin_name)
        model.set_value(iter, 0, value)

    def get_selected_plugin(self):
        treeview = self.ui['plugin_tree']
        selector = treeview.get_selection()
        model, iter = selector.get_selected()
        plugin_name = model.get_value(iter, 2)
        enabled = model.get_value(iter, 0)
        return plugin_name, enabled

    def select_plugin(self, treeview, event):
        plugin_name, enabled = self.get_selected_plugin()
        plugin = self.plugins[plugin_name]
        self.ui["plugin_description"].set_text(plugin.getDescription())
        widget = plugin.getUiWidget()
        plc_hld = self.ui["plugin_pref_placeholder"]
        for child in plc_hld.get_children():
            plc_hld.remove(child)
        if widget:
            widget.show()
            plc_hld.add(widget)

    def load_options_window(self):
        model = self.ui["liststore_plugins"]
        model.clear()
        self.ui["plugin_tree"].connect("button-release-event", self.select_plugin)
        self.ui["plugin_enabled_toggle"].connect("toggled", self.plugin_changed, model)
        for name in self.get_plugin_list():
            iter = model.append()
            enabled = name in self.pyazan.options.getEnabledPlugins()
            model.set(iter, 0, enabled, 1, name.capitalize(), 2, name)

    def save(self):
        #save enabled plugins
        index = 0
        enabled_plugins = list()
        model = self.ui["liststore_plugins"]
        for index in xrange(model.iter_n_children(None)):
            iter = model.iter_nth_child(None, index)
            plugin_name = model.get_value(iter, 2)
            enabled = model.get_value(iter, 0)
            if enabled:
                enabled_plugins.append(plugin_name)
        self.pyazan.options.setEnabledPlugins(enabled_plugins)
        for name in self.plugins:
            if self.plugins[name]:
                self.plugins[name].save()
