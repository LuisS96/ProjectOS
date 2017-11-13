import json
import os
from datetime import datetime
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
        self.pause = False
        self.finished = False
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
    current = next
    next = wait_queue.get()
    return current,next


def taquero(tacos_queue):
    global cycle
    cycle = 2
    wait_queue = Queue()
    current = tacos_queue.get()
    tacos_queue.task_done()
    while tacos_queue.empty() is False:
        next = tacos_queue.get()
        tacos_queue.task_done()
        current.qty -= cycle
        #According to size of order it forces to complete an order instead of increasing an overhead
        if current.qty == 1:
            current.qty -= cycle
        #While for switch
        while current.qty > 0:
            current,next = Switch(wait_queue,current,next)
            print('qty: ',current.qty,'id: ',current.Id)
            #Bonus cycles for huge orders
            if current.wcycle >= 8:
                current.qty -= cycle*4
            #Bonus cycles for big orders
            elif current.wcycle >= 6:
                current.qty -= cycle*3
            #Bonus cycles for medium orders
            elif current.wcycle >= 2:
                current.qty -= cycle*2
            #Small orders do not have bonus cycles
            else:
                current.qty -= cycle
            if current.qty == 1:
                current.qty -= cycle
        print(current)
        current = next
    #Finishing the last order
    while next.qty > 0:
        current = next
        current.qty -= cycle
    print(current)

# Thread_adobada = Thread(taquero(adobada_queue))
# Thread_others = Thread(taquero(others_queue))
# Thread_asada = Thread(taquero(asada_queue))
# Thread_others.setDaemon(True)
# Thread_asada.setDaemon(True)
# Thread_adobada.setDaemon(True)
# Thread_others.start()
# Thread_asada.start()
# Thread_adobada.start()


# TableThread_others.start()
raw_data = {'Queues': ['Asada', 'Adobada', 'Otros'],
            'Quantity': [asada_queue.qsize(), adobada_queue.qsize(), others_queue.qsize()]}
df = pd.DataFrame(raw_data, columns=['Queues', 'Quantity'])
print(df)


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


charts(df)
