import math
def datan(deg):
    return math.degrees(math.atan(deg))

def dsin(deg):
    return math.sin(math.radians(deg))

def dtan(deg):
    return math.tan(math.radians(deg))

def dacot(deg):
    return math.degrees(math.atan(1/deg))

def dcos(deg):
    return math.cos(math.radians(deg))

def dasin(deg):
    return math.degrees(math.asin(deg))

def dacos(deg):
    return math.degrees(math.acos(deg))

def datan2(x, y):
    return math.degrees(math.atan2(x, y))

def fixangle(a):
    a = a - 360.0 * (math.floor(a / 360.0));
    a = a + 360 if a < 0 else a;
    return a;
