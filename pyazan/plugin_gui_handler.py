import os, logging

from paths import getFullPath

class PluginGTK(object):
    def __init__(self, pyazan):
        self.ui = pyazan.ui
        self.pyazan = pyazan
        self.plugins = dict()
        self.load_plugins()

    def load_plugins(self):
        self.plugins = dict((name, list()) for name in self.get_plugin_list())
        for plugin_name in self.plugins.keys():
            if plugin_name in self.pyazan.options.getEnabledPlugins():
                self.enable_plugin(plugin_name)

    def get_plugin_list(self):
        plugindir = getFullPath("plugins")
        for file in os.listdir(plugindir):
            if os.path.isdir(os.path.join(plugindir, file)):
                yield file

    def enable_plugin(self, plugin_name):
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
            self.plugins[plugin_name].load(self.pyazan)
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
            plugin_name = model.get_value(iter, 1)
            if value:
                self.enablePlugin(plugin_name)
            else:
                self.disablePlugin(plugin_name)
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
        if plugin_name in self.plugins:
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
        model = self.ui["plugin_tree"].get_model()
        self.ui["plugin_tree"].connect("button-release-event", self.select_plugin)
        for k, v in self.plugins.iteritems():
            iter = model.append()
            enabled = k in self.pyazan.options.getEnabledPlugins()
            model.set(iter, 0, enabled, 1, k.capitalize(), 2, k)

    def save(self):
        for pl in self.plugins.itervalues():
            pl.save()
