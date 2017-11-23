from classes import *
from queue import *
import time as time
from datetime import datetime
from threading import Lock
from threading import Thread

lock = Lock()


# Checks order completion
def check_order(answersList, currentTaco):
    for answer in answersList:
        size = 0
        for suborder in answer.order.subordersList:
            if currentTaco.Id == suborder.Id:
                suborder.endTime = datetime.now()
                suborder.completed = True
            if suborder.completed:
                size += 1
                if size == answer.order.totalSubs and answer.order.completed is False:
                    answer.order.completed = True
                    answer.order.endTime = datetime.now()


def Switch(waitQueue, currentTaco, nextTaco):
    currentTaco.waitCycle += 1
    waitQueue.put(currentTaco)
    step = Steps("Pause", "Pausing suborder - sw", currentTaco.Id)
    currentTaco.steps.append(step)
    currentTaco = nextTaco
    if currentTaco.waitCycle == 0:
        currentTaco.startTime = datetime.now()
        step = Steps("Running", "Starting your suborder - sw", currentTaco.Id)
        currentTaco.steps.append(step)
    else:
        step = Steps("Resume", "Continuing suborder - sw", currentTaco.Id)
        currentTaco.steps.append(step)
    nextTaco = waitQueue.get()
    return currentTaco, nextTaco


def priority_check(currentTaco, tacos, tortillas, ingrQty):
    #step = Steps("Resume", "Continuing suborder - pc", currentTaco.Id)
    #currentTaco.steps.append(step)
    # Bonus cycles for huge orders
    if currentTaco.waitCycle >= 8:
        create_taco(tacos * 4, currentTaco, ingrQty, tortillas)
    # Bonus cycles for big orders
    elif currentTaco.waitCycle >= 6:
        create_taco(tacos * 3, currentTaco, ingrQty, tortillas)

    # Bonus cycles for medium orders
    elif currentTaco.waitCycle >= 2:
        create_taco(tacos * 2, currentTaco, ingrQty, tortillas)

    # Small orders do not have bonus cycles
    else:
        create_taco(tacos, currentTaco, ingrQty, tortillas)

    if currentTaco.tacosMade == 1:
        step = Steps("Resume", "Continuing suborder - pc", currentTaco.Id)
        currentTaco.steps.append(step)
        create_taco(1, currentTaco, ingrQty, tortillas)


def produce_tortillas(ingrQty, queue):  #Thread dependent of thread "taquero" that produces tortillas
    while not queue.empty():
        if ingrQty['tortillas'] >= 500:  # if there's more than 500 tortillas, keep producing tortillas and let the taquero take some
            with lock:
                ingrQty['tortillas'] += 1  # add 1 tortilla to the total, wasting a define interval of time
        else:
            while ingrQty['tortillas'] < 500:  # if there's less than 500 tortillas, make up to 50 tortillas and dont let the taquero take any
                with lock:
                    ingrQty['tortillas'] += 1
                time.sleep(.2)


def grab_tortillas(ingrQty):  # refill the taquero's tortillas with the tortillas made from the tortilera
    while ingrQty['tortillas'] < 500:
        time.sleep(.5)
    with lock:
        ingrQty['tortillas'] -= 500
        return 500


def create_taco(tacos, currentTaco, ingrQty, tortillas):
    madeTacos = 0
    while currentTaco.tacosMade > 0 and madeTacos < tacos:  # check if the order still has due tacos to avoid making extra iterations
        for ingredient in ingrQty:  # refill an ingredient when their qty is 0
            if ingredient == 'tortillas' and ingrQty[ingredient] == 0:
                step = Steps("Pause", "Refilling {0}".format(ingredient), currentTaco.Id)
                tortillas = grab_tortillas(ingrQty)
                step.endTime = datetime.now()
                currentTaco.steps.append(step)
                step = Steps("Resume", "Continuing suborder", currentTaco.Id)
                currentTaco.steps.append(step)
            if ingredient != 'tortillas' and ingrQty[ingredient] == 0:
                step = Steps("Pause", "Refilling {0}".format(ingredient), currentTaco.Id)
                ingrQty[ingredient] = 500
                time.sleep(0.5)
                step.endTime = datetime.now()
                currentTaco.steps.append(step)
                step = Steps("Resume", "Continuing suborder", currentTaco.Id)
                currentTaco.steps.append(step)
            tortillas -= 1  # subtract the ingredients used in the taco
            if ingredient != 'tortillas' and ingredient in str(currentTaco.ingr):
                ingrQty[ingredient] -= 1
        time.sleep(.1) # it takes the taquero 0.1 seconds to make a taco
        madeTacos += 1 # count of tacos made
        currentTaco.tacosMade -= 1 # substract 1 taco from the order



def taquero(queue, answersList, ingrQty):  # Each "taquero" represents a thread
    threadTortillera = Thread(target=produce_tortillas, args=(ingrQty, queue), daemon=True)  # Creates thread tortillera, produces the tortillas
    threadTortillera.start()
    tacos = 2  # Amount of tacos that a "taquero" can make at a time.
    tortillas = grab_tortillas(ingrQty)  # quantity of tacos that a taquero has
    waitQueue = Queue()  # Queue for our taquero of remaining orders
    if not queue.empty():
        currentTaco = queue.get()  # suborder in process
        while not queue.empty() or not waitQueue.empty():
            if queue.empty():
                nextTaco = waitQueue.get()
            if not queue.empty():
                nextTaco = queue.get()  # next suborder
            if currentTaco.qty == currentTaco.tacosMade:
                currentTaco.startTime = datetime.now()
                step = Steps("Running", "Starting your suborder - not", currentTaco.Id)
                currentTaco.steps.append(step)
                create_taco(tacos, currentTaco, ingrQty, tortillas)
            else:
                step = Steps("Resume", "Continuing suborder - not", currentTaco.Id)
                currentTaco.steps.append(step)
                priority_check(currentTaco, tacos, tortillas, ingrQty)
            if currentTaco.tacosMade == 1:
                step = Steps("Resume", "Continuing suborder - not", currentTaco.Id)
                currentTaco.steps.append(step)
                create_taco(1, currentTaco, ingrQty, tortillas)
            # While for switch
            if waitQueue.qsize() == 5 or queue.empty():
                while currentTaco.tacosMade > 0:
                    currentTaco, nextTaco = Switch(waitQueue, currentTaco, nextTaco)
                    priority_check(currentTaco,tacos,tortillas,ingrQty)
            if currentTaco.tacosMade > 0:
                waitQueue.put(currentTaco)  # Used to insert more suborders in the wait Queue.
                currentTaco.waitCycle += 1
                step = Steps("Pause", "Pausing suborder - first", currentTaco.Id)
                currentTaco.steps.append(step)
            if currentTaco.tacosMade == 0:
                step = Steps("Completed", "Suborder finished", currentTaco.Id)
                currentTaco.steps.append(step)
                check_order(answersList, currentTaco)
            currentTaco = nextTaco
        while currentTaco.tacosMade > 0:
            if currentTaco.waitCycle == 0 and currentTaco.tacosMade == currentTaco.qty:
                currentTaco.startTime = datetime.now()
                step = Steps("Running", "Starting your suborder - md", currentTaco.Id)
                currentTaco.steps.append(step)
            else:
                step = Steps("Resume", "Continuing suborder - md", currentTaco.Id)
                currentTaco.steps.append(step)
            priority_check(currentTaco, tacos, tortillas, ingrQty)

        step = Steps("Completed", "Suborder finished", currentTaco.Id)
        currentTaco.steps.append(step)
        check_order(answersList, currentTaco)
        threadTortillera.join()
    else:
        pass
