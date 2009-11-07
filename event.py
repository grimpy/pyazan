
class Event(object):
    def __init__(self):
        self.__callbacks = []
    
    def addCallback(self, callback):
        self.__callbacks.append(callback)
    
    def removeCallback(self, callback):
        self.__callbacks.remove(callback)
    
    def fire(self, *args, **kwards):
        for call in self.__callbacks:
            try:
                call(*args, **kwards)
            except:
                print "Error in handler %s" % call