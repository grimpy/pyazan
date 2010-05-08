import datetime, math, logging, os
from stopwatch import isInSameDay
from angle import dsin, dtan, dacot, dcos, dasin, dacos, datan2, fixangle
from stopwatch import Alarm
from event import Event

PRAYER_NAMES = ['fajr','sunrise', 'duhr', 'asr', 'maghrib', 'isha']

def fixhour(a):
    a = a - 24.0 * (math.floor(a / 24.0));
    a = a+24.0 if a < 0 else a;
    return a;

def getHoursMin(hourdec):
    hour = int(hourdec)
    min = math.ceil((hourdec - hour)*(100)/(10)*(6))
    if min == 60:
        hour+=1
        min = 0
    if hour == 24:
        hour = 0
    return (hour, int(min))

def getTomorrow():
    now = datetime.datetime.now()
    return now + datetime.timedelta(1)


def getNexPrayerName(prayer):
    nextprayeridx = PRAYER_NAMES.index(prayer)+1
    if nextprayeridx > len(PRAYER_NAMES)-1:
        nextprayeridx = 0
    return PRAYER_NAMES[nextprayeridx]

def getPreviousPrayerName(prayer):
    prevprayerindex = PRAYER_NAMES.index(prayer)-1
    if prevprayerindex < 0:
        prevprayerindex = len(PRAYER_NAMES) -1
    return PRAYER_NAMES[prevprayerindex]

def getNextPrayer(pray_int, prayer=None):
    nextprayer = None
    now = datetime.datetime.now()
    if prayer:
        nextprayer = getNexPrayerName(prayer)
        prayertime = getattr(pray_int, nextprayer)
        if isInSameDay(prayertime, now):
            return nextprayer, prayertime
        pray_int.day = getTomorrow()
        prayertime = getattr(pray_int, nextprayer)
        return nextprayer, prayertime
    else:
        for prayer_name in PRAYER_NAMES:
            prt = getattr(pray_int, prayer_name)
            if isInSameDay(prt, now):
                return prayer_name, prt
        pray_int.day = getTomorrow()
        prayertime = getattr(pray_int, PRAYER_NAMES[0])
        return PRAYER_NAMES[0], prayertime


class Praytime(object):
    _location = None
    _day = None

    def __init__(self, location=None, day=datetime.datetime.now()):
        for praytime in PRAYER_NAMES:
            setattr(self, praytime, (0,0))
        self.location = location
        self.day = day

    def setLocation(self, location):
        if location:
            self._location = location
            self.calculatetimes()

    def setDay(self, day):
        if day:
            self._day = day
            self.calculatetimes()

    location = property(fset=setLocation, fget=lambda s: s._location)
    day = property(fset=setDay, fget=lambda s: s._day)

    def calculatetimes(self):
        if not self.day or not self.location:
            return
        day2000 = datetime.datetime(2000, 1, 1)
        d = (self.day-day2000).days
        g = fixangle(357.529 + 0.98560028* d);
        q = fixangle(280.459 + 0.98564736* d);
        L = fixangle(q + 1.915* dsin(g) + 0.020* dsin(2*g));

        R = 1.00014 - 0.01671* dcos(g) - 0.00014* dcos(2*g);
        e = 23.439 - 0.00000036* d;
        RA = datan2(dcos(e)* dsin(L), dcos(L))/ 15;
        RA = fixhour(RA)

        D = dasin(dsin(e)* dsin(L));  # declination of the Sun
        EqT = q/15 - RA;  # equation of time

        sunsetangle = 0.8333
        #get asr angle
        asrangle = -dacot(1 + dtan(int(self.location.latitude-D)))

        duhr = 12+self.location.timezone - self.location.longitude/15 - EqT
        Fajr = duhr - self.tfunc(D, self.location.latitude, 19.5)
        Isha = duhr + self.tfunc(D, self.location.latitude, 17.5)
        Asr = duhr + self.tfunc(D, self.location.latitude, asrangle)

        self.fajr = getHoursMin(Fajr)
        self.sunrise = getHoursMin(duhr - self.tfunc(D, self.location.latitude, sunsetangle))
        self.duhr = getHoursMin(duhr)
        self.maghrib = getHoursMin(duhr + self.tfunc(D, self.location.latitude, sunsetangle))
        self.asr = getHoursMin(Asr)
        self.isha = getHoursMin(Isha)


    def tfunc(self, D, lati, angle):
        Z = (1.0/15) * dacos((-dsin(angle)-dsin(D)*dsin(lati))/(dcos(lati)*dcos(D)))
        return Z

    def __str__(self):
        if not self.location:
            return "Please configure location!"
        daystring = self.day.strftime("<u>%a %d %B</u>")
        strrepr = [daystring, ""]
        for praytime in PRAYER_NAMES:
            timetuple = getattr(self,praytime)
            timestring = "%02d:%02d" % (timetuple[0], timetuple[1])
            strrepr.append("%-14s\t%s" % (praytime.capitalize(), timestring))
        return "\n".join(strrepr)

if os.environ.get("DEBUG"):
    from test.test import Praytime

class PrayerTimesNotifier(object):
    def __init__(self, location, alert_on):
        self.praytime = Praytime(location)
        self.waitingfor = getNextPrayer(self.praytime)
        prayername = getPreviousPrayerName(self.waitingfor[0])
        self.now = (prayername, getattr(self.praytime, prayername))
        self.running = False
        self.alarm = Alarm()
        self._ontime = Event()
        self.alert_on = alert_on

    @property
    def onTime(self):
        return self._ontime

    def start(self):
        """
        Start notifying on prayers times
        """
        if self.waitingfor == self.now or not self.running:
            self.waitingfor = getNextPrayer(self.praytime, self.now[0])
            logging.info("Adding alarm %s", self.waitingfor)
            self.alarm.addAlarm(self.waitingfor[1], self._notify, self.waitingfor[0], self.waitingfor[1])
        self.running = True
        return True

    def _notify(self, *args):
        self.now = self.waitingfor
        if self.waitingfor[0] in self.alert_on:
            self._ontime.fire(*args)
        self.start()

    def __str__(self):
        return str(self.praytime)

    def __repr__(self):
        return str(self)
