import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from queue import *

tacos_asada = Queue()
tacos_otros = Queue()
tacos_adobada = Queue()

class Orden():
    def __init__(self, Id, Type, meat, qty, ingr, to_go = False):
        self.Id = Id
        self.priority=0
        self.time = str(datetime.now())
        self.Type = Type
        self.meat = meat
        self.qty = qty
        self.ingr = ingr
        self.to_go = to_go
        print('ID: ', Id, '\nType: ', Type, '\nMeat: ', meat, '\nQuantity: ', qty,'\n')

def read_order():
    with open ('test.txt') as jsfl: #reads file json
        data = json.load(jsfl)
    for d in data: #for each order there is
        print('\nNew Order','\nID: ', d['request_id'], '        ',d['datetime'], '\n')
        for i in d['orden']: #sub-array of each order that will be addeded to a queue.
            tacos = Orden(i['part_id'], i['type'], i['meat'], i['quantity'], i['ingredients'])
            if tacos.meat == "asada":
                tacos_asada.put(d)
            elif tacos.meat == "adobada":
                tacos_adobada.put(d)
            else:
                tacos_otros.put(d)
    setPriority()
            
read_order()
def setPriority():
    with open ('test.txt') as jsfl:#read json file
        data = json.load(jsfl)
    for o in data:#get every order
        for i in o['orden']:
            d = Orden(i['part_id'], i['type'], i['meat'], i['quantity'], i['ingredients'])
            if d.qty <= 0:#first priority fix based on tacos cuantity in order
                return "La orden esta vacia"
            if d.qty > 0 and d.qty <= 6:
                d.priority = 0
            elif d.qty > 6 and d.qty <= 12:
                d.priority = 1
            else:
                d.priority == 2
            print("Priority: ", d.priority)#show the fixed priority


#Table
raw_data= {'Queues': ['Asada', 'Adobada', 'Otros'],
           'Quantity': [tacos_asada.qsize(),tacos_adobada.qsize(),tacos_otros.qsize()]}
df = pd.DataFrame(raw_data, columns = ['Queues', 'Quantity'])
print(df)

def pie_chart():
    colors = ["cornflowerblue", "orangered", "gold"]
    plt.pie(
        df['Quantity'],
        labels=df['Queues'],
        shadow=False,
        colors=colors,
        startangle=90,
        autopct='%1.1f%%',
        )
    plt.axis('equal')

    plt.tight_layout()
    plt.show()

def bar_chart():
    length = list(range(len(df["Quantity"])))
    fig, ax = plt.subplots(figsize=(10,5))
    plt.bar([p + .375 for p in length],
            df["Quantity"],
            0.25,
            color="orangered",
            label=df["Queues"]
            )
    ax.set_ylabel('Total')
    ax.set_title('Tacos')
    ax.set_xticks([p + 1.5 * 0.25 for p in length])
    ax.set_xticklabels(df['Queues'])

    plt.xlim(min(length)-.25, max(length)+0.25*4)
    plt.ylim([0, max(df['Quantity']) + 1])
    plt.grid()
    plt.show()


pie_chart()
bar_chart()
