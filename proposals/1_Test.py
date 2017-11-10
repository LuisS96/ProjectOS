import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from queue import *
from threading import Thread

#Queues are created for their later use.
tacos_asada = Queue()
tacos_otros = Queue()
tacos_adobada = Queue()

#Class Orden is created as a parameter for each order received.
class Orden():
    def __init__(self, Id, Type, meat, qty, ingr, to_go = False):
        self.Id = Id
        self.priority = 0
        self.time = str(datetime.now())
        self.Type = Type
        self.meat = meat
        self.qty = qty
        self.ingr = ingr
        self.to_go = to_go
        #print('ID: ', Id, '\nType: ', Type, '\nMeat: ', meat, '\nQuantity: ', qty)
    def __str__(self): 
        return 'ID: {0} \nType: {1} \nMeat: {2} \nQuantity: {3} \nIngredients: {4} \nTo go: {5}'.format(self.Id, self.Type, self.meat, self.qty, self.ingr, self.to_go)
    def __iter__(self):
        return self

#Reads order from a list of dictionaries
def read_order():
    #In the time, we will be reading from a file named test.txt as if it was from an SQS message.
    with open ('test.txt') as jsfl: #reads file json
        data = json.load(jsfl)
    #First we count the amount of orders there are in our list of dictionaries. Each dictionary is classified by an order named 'order'.
    for d in data:
        print('\nNew Order','\nID: ', d['request_id'], '        ',d['datetime'], '\n')
        #We read each dictionary.
        for i in d['orden']: #sub-array of each order that will be addeded to a queue.
            tacos = Orden(i['part_id'], i['type'], i['meat'], i['quantity'], i['ingredients'])
            if tacos.meat == "asada":
                tacos_asada.put(d)
            elif tacos.meat == "adobada":
                tacos_adobada.put(d)
            else:
                tacos_otros.put(d)
            c = int(tacos.qty)
            if c <= 0:#First priority fix based on tacos quantity in order
                return "La orden esta vacia"
            if (c > 0) and (c <= 6):
                tacos.priority = 1
            elif (c > 6) and (c <= 12):
                tacos.priority = 2
            else:
                tacos.priority = 3
            print(tacos ,"\nPriority: ", tacos.priority,'\n')
            
read_order()

#Table
raw_data= {'Queues': ['Asada', 'Adobada', 'Otros'],
           'Quantity': [tacos_asada.qsize(),tacos_adobada.qsize(),tacos_otros.qsize()]}
df = pd.DataFrame(raw_data, columns = ['Queues', 'Quantity'])
print(df)

#Receives a DataFrame of at least two keys and two columns
#In our case, our pie is determined with our column 'Quantity'
#Pie chart and bar chart
def charts(df):
    plt.style.use("dark_background")
    colors = ["cornflowerblue", "orangered", "gold","r","limegreen","m","b","coral","yellow"]
    fig, axes = plt.subplots(ncols = 2,figsize=(10,10))
    ax1,ax2 = axes.ravel()

    #Pie chart
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

    #Bar chart
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

    #Both charts will be printed in one space and not one for each.
    plt.xlim(min(length)-.25, max(length)+0.25*4)
    plt.ylim([0, max(df['Quantity']) + 1])
    plt.grid()
    fig.tight_layout()
    fig.subplots_adjust(hspace=100)
    plt.show()

charts(df)



