import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from queue import *

class Orden():
    def __init__(self, Id, Type, meat, qty, ingr, to_go = False):
        self.Id = Id
        self.time = str(datetime.now())
        self.Type = Type
        self.meat = meat
        self.qty = qty
        self.ingr = ingr
        self.to_go = to_go
        print('ID: ', Id, '\nType: ', Type, '\nMeat: ', meat, '\nQuantity: ', qty,'\n')

def read_order():
    with open ('test.txt') as jsfl:
        data = json.load(jsfl)
    for d in data:
        print('\nNew Order','\nID: ', d['request_id'], '        ',d['datetime'], '\n')
        for i in d['orden']:
            Orden(i['part_id'], i['type'], i['meat'], i['quantity'], i['ingredients'])


read_order()
