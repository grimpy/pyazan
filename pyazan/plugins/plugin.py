class Plugin(object):
    def __init__(self):
        pass

    def load(self, *args):
        raise NotImplementedError

    def unload(self, *args):
        raise NotImplementedError

    def getDescription(self):
        return "No description"

    def getUiWidget(self):
        return None

    def save(self):
        print "Save Not implemented %s" %  self
        pass
