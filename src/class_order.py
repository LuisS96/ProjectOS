from datetime import datetime

# Class order is created as a parameter for each order received.
class orden():
    def __init__(self, Id, time):
        self.Id = Id  # integer
        self.time = time  # datetime
        self.list_subs = []  # List of suborders to check if completed
    def __str__(self):
        return 'ID: {0} \nTime: {1}'.format(self.Id, self.time)

class suborden():
    def __init__(self, Id, Type, meat, qty, ingr, to_go=False):
        self.Id = Id  # string
        self.time = str(datetime.now())  # time
        self.Type = Type  # string
        self.meat = meat  # string
        self.qty = int(qty)  # integer
        self.ingr = ingr  # string
        self.to_go = to_go  # boolean
        self.wcycle = 0  # integer - waited cycles

    def __str__(self):
        return 'ID: {0} \nType: {1} \nMeat: {2} \nQuantity: {3} \nIngredients: {4} \nTo go: {5}'.format(self.Id,self.Type,self.meat,self.qty,self.ingr,self.to_go)