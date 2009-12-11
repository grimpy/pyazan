class Plugin(object):
    def __init__(self):
        pass

    def load(self, *args):
        raise NotImplementedError

    def unload(self, *args):
        raise NotImplementedError
