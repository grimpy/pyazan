#import libnotify
import time
import threading
import datetime
import glib


def isInSameDay(timearg, refdate):
    return not (refdate.hour > timearg[0] or (refdate.hour == timearg[0] and refdate.minute > timearg[1]))

def convertToEpoch(timearg):
    if isinstance(timearg, (float, int)):
        return timearg
    elif  isinstance(timearg, (tuple,list)):
        if len(timearg) == 2:
            refdate = datetime.datetime.now()
            if not isInSameDay(timearg, refdate):
                refdate = refdate+ datetime.timedelta(1)
            timearg = datetime.datetime(refdate.year, refdate.month, refdate.day, timearg[0], timearg[1])
            return int(timearg.strftime("%s"))
    elif isinstance(timearg, datetime.datetime):
        return int(timearg.strftime("%s"))


class Alarm():
    def __init__(self):
        self.alarms = dict()

    def addAlarm(self, timearg, func, *args, **kwargs):
        delta = convertToEpoch(timearg) - time.time()
        if delta < 0:
            delta = 0
        return glib.timeout_add_seconds(int(delta), func, args, kwargs)

    def getAlarm(self, timearg):
        if timearg in self.alarms:
            return self.alarms.pop(timearg)
        return

    def stopAlarm(self, timearg):
        timer = self.getAlarm(timearg)
        if timer:
            timer.cancel()

    def waitForAlarm(self, timearg):
        timer = self.getAlarm(timearg)
        if timer:
            timer.join()

if __name__ == '__main__':
    def testfunc(a):
        print a
    a = Alarm()
    a.addAlarm(time.time()+5, testfunc, "Print me")
    time.sleep(7)