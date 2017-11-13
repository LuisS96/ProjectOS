from threading import Lock
from threading import Timer
import time as time
from datetime import datetime
from queue import *

lock = Lock()

#Checks order for completion by checking current ID
def check_order(order_list,current):
    for order in order_list:
        if current.Id in order.list_subs:
            order.list_subs.remove(current.Id)
            if not order.list_subs:
                order.endTime = datetime.now()
                print('ID: ', order.Id, '\tStatus: Order Finished')

#Switches current suborder to the threads wait queue and places the next suborder as current.
def Switch(wait_queue,current,next):
    current.wcycle += 1
    wait_queue.put(current)
    print('ID: ', current.Id, '\tStatus: Pause...', )
    current = next
    print('ID: ', current.Id, '\tStatus: Resume...', )
    next = wait_queue.get()
    return current,next


def starting_tortillas(starting_amount): #define the starting amount of tortillas the tortillera has
    global tortillera_tortillas
    tortillera_tortillas = starting_amount
    
def produce_tortillas(time_to_produce,tacos_queue): #define the time the tortillera needs to produce a single tortilla
    global tortillera_tortillas
    if tortillera_tortillas >= 50: #if there's more than 50 tortillas, keep producing tortillas and let the taquero take some
        with lock:
            tortillera_tortillas += 1 #add 1 tortilla to the total, wasting a define interval of time
        
    else:
        while tortillera_tortillas < 50: #if there's less than 50 tortillas, make up to 50 tortillas and dont let the taquero take any
            with lock:
                tortillera_tortillas += 1
            time.sleep(time_to_produce)
    if tacos_queue.empty() is False:
        tortillera = Timer(time_to_produce, produce_tortillas,[time_to_produce,tacos_queue]).start()


def grab_tortillas(interval): #refull the taquero's tortillas with the tortillas made from the tortilera
    global tortillera_tortillas
    if tortillera_tortillas > 50:
        with lock:
            tortillera_tortillas -= 50
            
    else:
        time.sleep(interval)
        grab_tortillas(interval)

def make_taco(guacamole,cilantro,salsa,cebolla,frijol,tortillas,cycle,current,made_tacos):
    while current.qty > 0: #check if the order still has due tacos to avoid making extra iterations
        if tortillas == 0: #refill an ingredient when their qty is 0
            print('ID: ', current.Id, '\tStatus: Pause...', "refilling tortillas", )
            grab_tortillas(.5)
            tortillas = 50
            print('ID: ', current.Id, '\tStatus: Resume...', )
        if cilantro == 0:
            print('ID: ', current.Id, '\tStatus: Pause...', "refilling cilantro", )
            cilantro = 500
            time.sleep(0.5)
            print('ID: ', current.Id, '\tStatus: Resume...', )
        if cebolla == 0:
            print('ID: ', current.Id, '\tStatus: Pause...', "refilling cebolla", )
            cebolla = 500
            time.sleep(0.5)
            print('ID: ', current.Id, '\tStatus: Resume...', )
        if guacamole == 0:
            print('ID: ', current.Id, '\tStatus: Pause...', "refilling guacamole", )
            guacamole = 500
            time.sleep(0.5)
            print('ID: ', current.Id, '\tStatus: Resume...', )
        if salsa == 0:
            print('ID: ', current.Id, '\tStatus: Pause...', "refilling salsa", )
            salsa = 500
            time.sleep(0.5)
            print('ID: ', current.Id, '\tStatus: Resume...', )
        tortillas -= 1 #substract the ingredients used in the taco
        if "cebolla" in current.ingr: 
            cebolla -= 1
        if "guacamole" in current.ingr:
            guacamole -= 1
        if "salsa" in current.ingr:
            salsa -= 1
        if "frijol" in current.ingr:
            frijol -= 1
        if "cilantro" in current.ingr:
            cilantro -= 1
        time.sleep(.1) #it takes the taquero 0.1 seconds to make a taco
        made_tacos += 1 #count of tacos made
        current.qty -= 1 #substract 1 taco from the order
        if made_tacos < cycle:
            make_taco(guacamole,cilantro,salsa,cebolla,frijol,tortillas,cycle,current,made_tacos)
        else:
            break
    return guacamole,cilantro,salsa,cebolla,frijol,tortillas

def taquero(tacos_queue, order_list):
    starting_tortillas(500) #define starting quantities for every ingredient
    produce_tortillas(.01,tacos_queue)
    cycle = 2
    guacamole = 10
    salsa = 10
    cebolla = 10
    cilantro = 10
    frijol = 10
    tortillas = 10
    wait_queue = Queue()
    current = tacos_queue.get()
    while tacos_queue.empty() is False:
        print('ID: ', current.Id, '\tStatus: Starting your suborder of tacos...')
        time.sleep(1)
        guacamole,cilantro,salsa,cebolla,frijol,tortillas = make_taco(guacamole,cilantro,salsa,cebolla,frijol,tortillas,cycle,current,0)
        next = tacos_queue.get()
        #According to size of order it forces to complete an order instead of increasing an overhead
        if current.qty == 1:
            guacamole,cilantro,salsa,cebolla,frijol,tortillas = make_taco(guacamole,cilantro,salsa,cebolla,frijol,tortillas,1,current,0)
        #While for switch
        while current.qty > 0:
            current,next = Switch(wait_queue,current,next)
            #Bonus cycles for huge orders
            if current.wcycle >= 8:
                guacamole,cilantro,salsa,cebolla,frijol,tortillas = make_taco(guacamole,cilantro,salsa,cebolla,frijol,tortillas,cycle*4,current,0)
            #Bonus cycles for big orders
            elif current.wcycle >= 6:
                guacamole,cilantro,salsa,cebolla,frijol,tortillas = make_taco(guacamole,cilantro,salsa,cebolla,frijol,tortillas,cycle*3,current,0)
            #Bonus cycles for medium orders
            elif current.wcycle >= 2:
                guacamole,cilantro,salsa,cebolla,frijol,tortillas = make_taco(guacamole,cilantro,salsa,cebolla,frijol,tortillas,cycle*2,current,0)
            #Small orders do not have bonus cycles
            else:
                guacamole,cilantro,salsa,cebolla,frijol,tortillas = make_taco(guacamole,cilantro,salsa,cebolla,frijol,tortillas,cycle,current,0)
            if current.qty == 1:
                guacamole,cilantro,salsa,cebolla,frijol,tortillas = make_taco(guacamole,cilantro,salsa,cebolla,frijol,tortillas,1,current,0)
        print('ID: ', current.Id, '\tStatus: Suborder finished')
        check_order(order_list, current)
        current = next
    #Finishing the last order
    while next.qty > 0:
        current = next
        guacamole,cilantro,salsa,cebolla,frijol,tortillas = make_taco(guacamole,cilantro,salsa,cebolla,frijol,tortillas,cycle,current,0)
    print('ID: ', current.Id, '\tStatus: Resume...')
    print('ID: ', current.Id, '\tStatus: Suborder finished')
    check_order(order_list, current)



