from classes import *
from queue import *
import time as time
from datetime import datetime
from threading import Lock
from threading import Timer

lock = Lock()


# Checks order for completion by checking current ID
def check_order(answersList, currentTaco, countSteps, stepsList):
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
                    step = Steps(countSteps, "Completed", "Order finished", currentTaco.Id)
                    stepsList.append(step)
                    print(step)
                    # print('ID: ', order.Id, '\tStatus: Order Finished')
                    answer.steps == stepsList
                    stepsList.clear()


def Switch(waitQueue, currentTaco, nextTaco, countSteps, stepsList):
    currentTaco.waitCycle += 1
    waitQueue.put(currentTaco)
    countSteps += 1
    step = Steps(countSteps, "Pause", "Entered wait queue", currentTaco.Id)
    stepsList.append(step)
    print(step)
    # print('ID: ', currentTaco.Id, '\tStatus: Pause...', )
    currentTaco = nextTaco
    # print('ID: ', currentTaco.Id, '\tStatus: Resume...', )
    countSteps += 1
    step = Steps(countSteps, "Resume", "Left wait queue", currentTaco.Id)
    stepsList.append(step)
    print(step)
    nextTaco = waitQueue.get()
    return currentTaco, nextTaco, countSteps


def starting_tortillas(starting_amount):  # define the starting amount of tortillas the tortillera has
    global tortillera_tortillas
    tortillera_tortillas = starting_amount


def produce_tortillas(time_to_produce, tacos_queue):  # define the time the tortillera needs to produce a single tortilla
    global tortillera_tortillas
    if tortillera_tortillas >= 500:  # if there's more than 50 tortillas, keep producing tortillas and let the taquero take some
        with lock:
            tortillera_tortillas += 1  # add 1 tortilla to the total, wasting a define interval of time

    else:
        while tortillera_tortillas < 500:  # if there's less than 50 tortillas, make up to 50 tortillas and dont let the taquero take any
            with lock:
                tortillera_tortillas += 1
            time.sleep(time_to_produce)
    if tacos_queue.empty() is False:
        tortillera = Timer(time_to_produce, produce_tortillas, [time_to_produce, tacos_queue]).start()


def grab_tortillas(interval):  # refull the taquero's tortillas with the tortillas made from the tortilera
    global tortillera_tortillas
    if tortillera_tortillas > 500:
        with lock:
            tortillera_tortillas -= 500

    else:
        time.sleep(interval)
        grab_tortillas(interval)


def create_taco(countSteps, tacos, currentTaco, stepsList, tortillas, guacamole, cilantro, cebolla, frijol, salsa, madeTacos):
    while currentTaco.qty > 0: #check if the order still has due tacos to avoid making extra iterations
        if tortillas == 0: #refill an ingredient when their qty is 0
            countSteps += 1
            step = Steps(countSteps, "Pause", "Refilling tortillas", currentTaco.Id)
            # print('ID: ', current.Id, '\tStatus: Pause...', "refilling tortillas", )
            grab_tortillas(.5)
            tortillas = 50
            step.endTime = datetime.now()
            stepsList.append(step)
            print(step)
            countSteps += 1
            step = Steps(countSteps, "Resume", "Continuing suborder", currentTaco.Id)
            stepsList.append(step)
            print(step)
            # print('ID: ', current.Id, '\tStatus: Resume...', )
        if cilantro == 0:
            countSteps += 1
            step = Steps(countSteps, "Pause", "Refilling cilantro", currentTaco.Id)
            # print('ID: ', current.Id, '\tStatus: Pause...', "refilling cilantro", )
            cilantro = 500
            time.sleep(0.5)
            step.endTime = datetime.now()
            stepsList.append(step)
            print(step)
            countSteps += 1
            step = Steps(countSteps, "Resume", "Continuing suborder", currentTaco.Id)
            stepsList.append(step)
            print(step)
            # print('ID: ', current.Id, '\tStatus: Resume...', )
        if cebolla == 0:
            countSteps += 1
            step = Steps(countSteps, "Pause", "Refilling cebolla", currentTaco.Id)
            # print('ID: ', current.Id, '\tStatus: Pause...', "refilling cebolla", )
            cebolla = 500
            time.sleep(0.5)
            step.endTime = datetime.now()
            stepsList.append(step)
            print(step)
            countSteps += 1
            step = Steps(countSteps, "Resume", "Continuing suborder", currentTaco.Id)
            stepsList.append(step)
            print(step)
            # print('ID: ', current.Id, '\tStatus: Resume...', )
        if guacamole == 0:
            countSteps += 1
            step = Steps(countSteps, "Pause", "Refilling guacamole", currentTaco.Id)
            # print('ID: ', current.Id, '\tStatus: Pause...', "refilling guacamole", )
            guacamole = 500
            time.sleep(0.5)
            step.endTime = datetime.now()
            stepsList.append(step)
            print(step)
            countSteps += 1
            step = Steps(countSteps, "Resume", "Continuing suborder", currentTaco.Id)
            stepsList.append(step)
            print(step)
            # print('ID: ', current.Id, '\tStatus: Resume...', )
        if salsa == 0:
            countSteps += 1
            step = Steps(countSteps, "Pause", "Refilling salsa", currentTaco.Id)
            # print('ID: ', current.Id, '\tStatus: Pause...', "refilling salsa", )
            salsa = 500
            time.sleep(0.5)
            step.endTime = datetime.now()
            stepsList.append(step)
            print(step)
            countSteps += 1
            step = Steps(countSteps, "Resume", "Continuing suborder", currentTaco.Id, currentTaco.startTime)
            stepsList.append(step)
            print(step)
            # print('ID: ', current.Id, '\tStatus: Resume...', )
        tortillas -= 1 #substract the ingredients used in the taco
        if "Cebolla" in currentTaco.ingr:
            cebolla -= 1
        if "Guacamole" in currentTaco.ingr:
            guacamole -= 1
        if "Salsa" in currentTaco.ingr:
            salsa -= 1
        if "Frijol" in currentTaco.ingr:
            frijol -= 1
        if "Cilantro" in currentTaco.ingr:
            cilantro -= 1
        time.sleep(.1) #it takes the taquero 0.1 seconds to make a taco
        madeTacos += 1 #count of tacos made
        currentTaco.qty -= 1 #substract 1 taco from the order
        if madeTacos < tacos:
            create_taco(countSteps, tacos, currentTaco, stepsList, tortillas, guacamole, cilantro, cebolla, frijol, salsa, madeTacos)
        else:
            break
    return guacamole, cilantro, salsa, cebolla, frijol, tortillas


def taquero(queue, answersList):  # Each "taquero" represents a thread
    tacos = 2  # Amount of tacos that a "taquero" can make at a time.
    tortillas = 500
    guacamole = 500
    cilantro = 500
    cebolla = 500
    frijol = 500
    salsa = 500
    waitQueue = Queue()
    stepsList = []
    countSteps = 1
    if not queue.empty():
        currentTaco = queue.get()
        currentTaco.startTime = datetime.now()
        step = Steps(countSteps, "Running", "Starting your suborder", currentTaco.Id)
        print(step)
        stepsList.append(step)
        while not queue.empty():
            nextTaco = queue.get()
            time.sleep(1)
            guacamole, cilantro, salsa, cebolla, frijol, tortillas = create_taco(countSteps, tacos, currentTaco, stepsList, tortillas, guacamole,
                                                                                 cilantro, cebolla, frijol, salsa, 0)
            if currentTaco.qty == 1:
                guacamole, cilantro, salsa, cebolla, frijol, tortillas = create_taco(countSteps, 1, currentTaco, stepsList, tortillas, guacamole,
                                                                                     cilantro, cebolla, frijol, salsa, 0)
            # While for switch
            while currentTaco.qty > 0:
                currentTaco, nextTaco, countSteps = Switch(waitQueue, currentTaco, nextTaco, countSteps, stepsList)
                # Bonus cycles for huge orders
                if currentTaco.waitCycle >= 8:
                    guacamole, cilantro, salsa, cebolla, frijol, tortillas = create_taco(countSteps, tacos * 4, currentTaco, stepsList, tortillas,
                                                                                       guacamole, cilantro, cebolla,
                                                                                       frijol, salsa, 0)
                # Bonus cycles for big orders
                elif currentTaco.waitCycle >= 6:
                    guacamole, cilantro, salsa, cebolla, frijol, tortillas = create_taco(countSteps, tacos * 3, currentTaco, stepsList, tortillas,
                                                                                       guacamole, cilantro, cebolla,
                                                                                       frijol, salsa, 0)

                # Bonus cycles for medium orders
                elif currentTaco.waitCycle >= 2:
                    guacamole, cilantro, salsa, cebolla, frijol, tortillas = create_taco(countSteps, tacos * 2, currentTaco, stepsList, tortillas,
                                                                                       guacamole, cilantro, cebolla,
                                                                                       frijol, salsa, 0)

                # Small orders do not have bonus cycles
                else:
                    guacamole, cilantro, salsa, cebolla, frijol, tortillas = create_taco(countSteps, tacos, currentTaco, stepsList, tortillas,
                                                                                       guacamole, cilantro, cebolla,
                                                                                       frijol, salsa, 0)

                if currentTaco.qty == 1:
                    guacamole, cilantro, salsa, cebolla, frijol, tortillas = create_taco(countSteps, 1, currentTaco, stepsList, tortillas,
                                                                                       guacamole, cilantro, cebolla,
                                                                                       frijol, salsa, 0)
            step = Steps(countSteps, "Completed", "Suborder finished", currentTaco.Id)
            stepsList.append(step)
            print(step)
            check_order(answersList, currentTaco, countSteps, stepsList)
            currentTaco = nextTaco
            step = Steps(countSteps, "Running", "Starting your suborder", currentTaco.Id)
            print(step)
            stepsList.append(step)
        while currentTaco.qty > 0:
            guacamole, cilantro, salsa, cebolla, frijol, tortillas = create_taco(countSteps, tacos, currentTaco, stepsList, tortillas,
                                                                                 guacamole, cilantro, cebolla,
                                                                                 frijol, salsa, 0)
        step = Steps(countSteps, "Completed", "Suborder finished", currentTaco.Id)
        stepsList.append(step)
        print(step)
        check_order(answersList, currentTaco, countSteps,stepsList)
    else:
        pass