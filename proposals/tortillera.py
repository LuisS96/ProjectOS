from threading import Thread
from threading import Lock
import time
lock = Lock()
class tortillas(object):
    def __init__(self):
        self.value = 500
        self.lock = Lock()
    
    def increment(self):
        with self.lock:
            self.value += 1
tpt = tortillas()
def tortillear():
    if tpt.value >= 50:
        with lock:
            tpt.increment()
            print(tpt.value)
        time.sleep(.1)
        
    else:
        while tpt.value < 50:
            with lock:
                tpt.increment()
                print("ay mushashos ya van las tortillas")
            time.sleep(.1)
    tortillear()

def taquerear():
    if tpt.value > 50:
        with lock:
            tpt.value -= 50
            print("agarre tacos cuca")
        time.sleep(1)
    else:
        time.sleep(1)
    taquerear()

tortillera = Thread(target=tortillear)
tortillera.setDaemon=True
tortillera.start()
taquero = Thread(target=taquerear)
taquero.setDaemon=True
taquero.start()
ts = []
ts.append(tortillera)
ts.append(taquero)
for t in ts:
    t.join()
