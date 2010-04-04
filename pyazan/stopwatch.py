import time
import datetime
import gobject

DELTA_TIME = 60

def isInSameDay(timearg, refdate):
    if (refdate.hour < timearg[0]):
        return True
    if (refdate.hour == timearg[0] and refdate.minute <= timearg[1]):
        return True
    return False

def convertToEpoch(timearg):
    if isinstance(timearg, (float, int)):
        return timearg
    elif  isinstance(timearg, (tuple,list)):
        if len(timearg) == 2:
            refdate = datetime.datetime.now()
            if not isInSameDay(timearg, refdate):
                refdate = refdate + datetime.timedelta(1)
            timearg = datetime.datetime(refdate.year, refdate.month, refdate.day, timearg[0], timearg[1])
            return int(timearg.strftime("%s"))
    elif isinstance(timearg, datetime.datetime):
        return int(timearg.strftime("%s"))

def getTimeDiff(timearg):
    then = datetime.datetime.fromtimestamp(convertToEpoch(timearg))
    return then - datetime.datetime.now()

class Alarm():

    def addAlarm(self, timearg, func, *args, **kwargs):
        delta = convertToEpoch(timearg) - time.time()
        if delta < 0:
            delta = 0
        if delta > DELTA_TIME:
            args = list(args)
            args.insert(0, func)
            args.insert(0, timearg)
            func = self.addAlarm
            delta = DELTA_TIME
        gobject.timeout_add_seconds(int(delta), func, *args, **kwargs)

if __name__ == '__main__':
    def testfunc(a):
        print a
    a = Alarm()
    a.addAlarm(time.time()+5, testfunc, "Print me")
    time.sleep(7)
