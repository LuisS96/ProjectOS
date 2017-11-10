from datetime import datetime

#Class Orden is created as a parameter for each order received.
class Order():
    def __init__(self, Id, Type, meat, qty, ingr, to_go = False):
        self.Id = Id #integer
        self.priority = 0 #integer
        self.time = str(datetime.now()) #integer
        self.Type = Type #string
        self.meat = meat #string
        self.qty = qty #integer
        self.ingr = ingr #string
        self.to_go = to_go #boolean
        #print('ID: ', Id, '\nType: ', Type, '\nMeat: ', meat, '\nQuantity: ', qty)
    def __str__(self): 
        return 'ID: {0} \nType: {1} \nMeat: {2} \nQuantity: {3} \nIngredients: {4} \nTo go: {5}'.format(self.Id, self.Type, self.meat, self.qty, self.ingr, self.to_go)
    def __iter__(self):
        return self

