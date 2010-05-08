import gtk

class UiDict(dict):
    def __init__(self, file):
        self.builder = gtk.Builder()
        self.builder.add_from_file(file)
        self.cache = dict()

    def __getitem__(self, name):
        if name not in self.cache:
            self.cache[name] = self.builder.get_object(name)
        return self.cache[name]
