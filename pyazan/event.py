import logging

class Event(object):
    def __init__(self):
        self.__callbacks = []

    def addCallback(self, callback):
        self.__callbacks.append(callback)

    def removeCallback(self, callback):
        self.__callbacks.remove(callback)

    def hasCallback(self, callback):
        return callback in self.__callbacks

    def fire(self, *args, **kwargs):
        for call in self.__callbacks:
            try:
                call(*args, **kwargs)
            except Exception, e:
                logging.warning("Error in handler %s, errormsg %s", call, e)
