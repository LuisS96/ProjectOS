from threading import Lock
from threading import Timer
import time
lock = Lock()

def starting_tortillas(starting_amount): #define the starting amount of tortillas
    global tortillera_tortillas
    tortillera_tortillas = starting_amount
    
def produce_tortillas(time_to_produce): #define the time the tortillera need to produce a single tortilla
    global tortillera_tortillas
    
    if tortillera_tortillas >= 50: #if more than 50 tortillas, keep producing tortillas and let the taquero take some
        with lock:
            tortillera_tortillas += 1 #add 1 tortilla to the total, wasting a define interval of time
        
    else:
        while tortillera_tortillas < 50: #if less than 50 tortillas, make up to 50 tortillas and dont let the taquero take any
            with lock:
                tortillera_tortillas += 1
            time.sleep(time_to_produce)
    tortillera = Timer(time_to_produce, produce_tortillas,[time_to_produce]).start()

def grab_tortillas(interval): #refull the taquero's tortillas with the tortillas made from the tortilera
    global tortillera_tortillas
    
    if tortillera_tortillas > 50:
        with lock:
            tortillera_tortillas -= 50
            
    else:
        time.sleep(interval)
