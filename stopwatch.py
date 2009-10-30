#import libnotify
import time
import threading

class Stopwatch(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        time.sleep(5)
        print "Testing"

c = Stopwatch()
c.start()
print "Ikke eerst"
time.sleep(6)
    
