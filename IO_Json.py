import json
import datetime

todo = ['frijol', 'guacamole', 'cilantro', 'cebolla', 'salsa']
ingredientes = ['frijol', 'guacamole', 'cilantro', 'cebolla', 'salsa']

class Orden():
    counter = 0
    def __init__(self,taco='asada',cant=1,ingr=todo,llevar=False):
        self.Id = Orden.counter
        self.taco = taco
        self.cant = cant
        self.ingr = ingr
        self.time = str(datetime.datetime.now())
        self.llevar = llevar
        Orden.counter += 1
    def writing(self):
        print('Son ' + str(o.cant) + ' tacos de ' + str(o.taco) + ' con ' + str(o.ingr))
        orden = {'id':o.Id,'tacos': o.taco,'cantidad': o.cant,'ingredientes': o.ingr,'tiempo': o.time,'llevar':o.llevar}
        jsfl = json.dumps(orden, indent = 4,sort_keys=True)
        try:
            target = open('ordenes.txt','a')
            target.write(str(jsfl))
#            print(jsfl)
        except:
            print('Unexpected error')

o = Orden()

while True:
    backup = []
    print()
    o.taco = input('Tacos de: ')
    o.cant = input('Cuantos? ')
    ingred =  input('Con todo? ')
    if 'sin' in ingred:
        ingred = ingred.replace(',', ' ')
        ingred = ingred.split()
        for i in ingred:
            if i in todo:
               todo.remove(i)
               backup.append(i)
        o.ingr = todo
    elif 'si' in ingred or 'todo' in ingred:
        o.ingr = ingredientes
    else:
        ingredTemp = []
        ingred = input('    con que? ')
        ingred = ingred.replace(',',' ')
        ingred = ingred.replace('y',' ')
        ingred = ingred.split()
        for i in ingred:
            if i in ingredientes:
                ingredTemp.append(i)
        o.ingr = ingredTemp
    o.writing()


