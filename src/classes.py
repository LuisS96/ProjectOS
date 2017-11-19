__author__ = 'lfsc96'

from datetime import datetime


class Order:
    def __init__(self, Id, startTime):
        self.Id = Id  # String received from the SQS message
        self.startTime = datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")  # datetime received from the SQS message
        self.endTime = datetime.now()  # Will be replaced by the time it finishes
        self.subordersList = []  # List of suborders
        self.completed = False  # when completed, will changed to True
        self.totalSubs = 0  # Amount of suborders in order.

    def __str__(self):
        return 'datetime: {0} \nrequest_id: {1} \nOrder: {2}'.format(self.startTime, self.Id, self.subordersList)

    def __iter__(self):
        for suborder in self.subordersList:
            return suborder


class Suborder:
    def __init__(self, Id, Type, meat, qty, ingr):
        self.Id = Id  # String received from the SQS message
        self.startTime = datetime.now()
        self.endTime = datetime.now()  # Will be replaced by the time it finishes
        self.Type = Type  # Type of order, like quesadilla, taco, mulita, etc.
        self.meat = meat  # Type of meat for the order
        self.qty = int(qty)  # Quantity of tacos ordered
        self.ingr = ingr  # Ingredients
        self.to_go = False  # If it to go it will change
        self.waitCycle = 0  # Time waiting to be processed, used as priority condition
        self.completed = False  # When completed, will change to True

    def __str__(self):
        return 'ID: {0} \nType: {1} \nMeat: {2} \nQuantity: {3} \nIngredients: {4} \nTo go: {5}'.format(self.Id, self.Type, self.meat, self.qty, self.ingr, self.to_go)


class Answer:
    def __init__(self, order):
        # self.startTime = datetime.now()
        self.order = order
        # self.endTime = datetime.now()
        self.steps = []  # List of steps that an order gets to be completed

    def __str__(self):
        return '{0} \nanswer: {\nstart_time: {1} \nend_time{2} \nsteps: {3}}'.format(self.order, self.order.startTIme, self.order.endTime, self.steps)


class Steps:
    def __init__(self, step, state, action, Id):
        self.step = int(step)  # Number of steps that takes an order to be completed
        self.state = state  # Is it running or paused
        self.action = action
        self.Id = Id
        self.startTime = datetime.now()
        self.endTime = datetime.now()

    def __str__(self):
        return 'Step: {0} \nState: {1} \nAction: {2} \nID: {3} \nStartTime: {4} \nEndTime: {5}'.format(self.step, self.state, self.action, self.Id, self.startTime, self.endTime)
