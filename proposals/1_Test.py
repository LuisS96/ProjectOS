import json
import os
from datetime import datetime
from threading import Thread
from threading import Lock
from threading import Timer
import pandas as pd
import matplotlib.pyplot as plt
from queue import *
from threading import Thread
import time as time

# Class Orden is created as a parameter for each order received.
class Orden():
    def __init__(self, Id, Type, meat, qty, ingr, to_go=False):
        self.Id = Id #integer
        self.priority = 0 #integer
        self.time = str(datetime.now()) #time
        self.Type = Type #string
        self.meat = meat #string
        self.qty = int(qty) #integer
        self.ingr = ingr #string
        self.to_go = to_go #boolean
        self.wcycle = 0 #integer - waited cycles
        # print('ID: ', Id, '\nType: ', Type, '\nMeat: ', meat, '\nQuantity: ', qty)

    def __str__(self):
        return 'ID: {0} \nType: {1} \nMeat: {2} \nQuantity: {3} \nIngredients: {4} \nTo go: {5}'.format(self.Id,
                                                                                                        self.Type,
                                                                                                        self.meat,
                                                                                                        self.qty,
                                                                                                        self.ingr,
                                                                                                        self.to_go)
    def __iter__(self):
        return self

file = "Order.json"
lock = Lock()

def read_order(file):
    # Assures that the file exists and is located in the same directory
    if os.path.isfile(file) == False:
        print('The file "{0}" is not located in the same directory or does not exist.'.format(file))
        return
    else:
        # Creates file title into lowercase string and checks file extension if json
        if file.lower().endswith('.json'):
            # Trys to open the json file, an exception is raised if file can not be readen properly
            try:
                with open(file) as jsfl:
                    data = json.load(jsfl)
                return data
            except:
                print("Make sure your json file is correctly written")
        else:
            print('File type is not .json and cannot be readen')

# Queues are created for their later use.
asada_queue = Queue()
adobada_queue = Queue()
others_queue = Queue()

# Reads order from a list of dictionaries
def queues(data):
    # In the time, we will be reading from a file named test.txt as if it was from an SQS message.
    for order in data:
        # print('\nNew Order', '\nID: ', order['request_id'], '\t', 'time: ',order['datetime'], '\n')
        # We read each dictionary.
        for suborder in order['orden']: # sub-array of each order that will be addeded to a queue.
            tacos = Orden(suborder['part_id'], suborder['type'], suborder['meat'], suborder['quantity'], suborder['ingredients'])
            # print(tacos)
            if tacos.meat == 'asada':
                asada_queue.put(tacos)
            elif tacos.meat == 'adobada':
                adobada_queue.put(tacos)
            else:
                others_queue.put(tacos)

queues(read_order(file))

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

def taquero(tacos_queue):
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
        print('ID: ', current.Id, '\tStatus: Starting your order of tacos...', )
        time.sleep(1)
        guacamole,cilantro,salsa,cebolla,frijol,tortillas = make_taco(guacamole,cilantro,salsa,cebolla,frijol,tortillas,cycle,current,0)
        next = tacos_queue.get()
        #According to size of order it forces to complete an order instead of increasing an overhead
        if current.qty == 1:
            guacamole,cilantro,salsa,cebolla,frijol,tortillas = make_taco(guacamole,cilantro,salsa,cebolla,frijol,tortillas,1,current,0)
        #While for switch
        while current.qty > 0:
            current,next = Switch(wait_queue,current,next)
            print('qty: ',current.qty,'id: ',current.Id)
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
        print('ID: ', current.Id, '\tStatus: Finished', )
        # print('\n',current)
        current = next
    #Finishing the last order
    while next.qty > 0:
        current = next
        guacamole,cilantro,salsa,cebolla,frijol,tortillas = make_taco(guacamole,cilantro,salsa,cebolla,frijol,tortillas,cycle,current,0)
    print('ID: ', current.Id, '\tStatus: Resume...', )
    print('ID: ', current.Id, '\tStatus: Finished', )
    # print(current)



#parallel threading
def Throw_Threads(asada_queue, adobada_queue, others_queue):

    queue_list = [asada_queue, adobada_queue, others_queue]
    thread_list = []

    for t in queue_list:
        thread = Thread(target=taquero, args=(t,), daemon=True)
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()

    raw_data = {'Queues': ['Asada', 'Adobada', 'Otros'],
                'Quantity': [asada_queue.qsize(), adobada_queue.qsize(), others_queue.qsize()]}
    df = pd.DataFrame(raw_data, columns=['Queues', 'Quantity'])
    print(df)
    return df


# Receives a DataFrame of at least two keys and two columns
# In our case, our pie is determined with our column 'Quantity'
# Pie chart and bar chart
def charts(df):
    plt.style.use("dark_background")
    colors = ["cornflowerblue", "orangered", "gold", "r", "limegreen", "m", "b", "coral", "yellow"]
    fig, axes = plt.subplots(ncols=3, figsize=(15, 10))
    ax1, ax2, ax3 = axes.ravel()

    # Table
    meat = []
    for i in df['Quantity']:
        meat.append([i])
    columns = ['Quantity']
    rows = ['Asada', 'Adobada', 'Otros']
    ax3.axis('off')
    table = ax3.table(cellText=meat,
                      cellColours=[['black'] * len(meat[0])] * len(meat),
                      colLabels=columns,
                      colColours=['black'] * len(columns),
                      rowLabels=rows,
                      rowColours=colors,
                      loc='center')
    table.scale(.3, 1.5)

    # Pie chart
    ax1.pie(
        df['Quantity'],
        labels=df['Queues'],
        shadow=False,
        colors=colors,
        startangle=90,
        autopct='%1.1f%%',
    )
    ax1.axis('equal')
    ax1.margins(1)

    # Bar chart
    length = list(range(len(df["Quantity"])))
    ax2.bar([p + .375 for p in length],
            df["Quantity"],
            0.25,
            color="orangered",
            label=df["Queues"]
            )
    ax2.set_ylabel('Total')
    ax2.set_title('Tacos')
    ax2.set_xticks([p + 1.5 * 0.25 for p in length])
    ax2.set_xticklabels(df['Queues'])

    # Both charts will be printed in one space and not one for each.
    plt.xlim(min(length) - .25, max(length) + 0.25 * 4)
    plt.ylim([0, max(df['Quantity']) + 1])
    plt.grid()
    fig.tight_layout()
    fig.subplots_adjust(hspace=100)
    plt.show()


charts(Throw_Threads(asada_queue, adobada_queue, others_queue))
