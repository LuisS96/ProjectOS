__author__ = 'lfsc96'

from datetime import datetime


class Order:
    suborders = []

    def __init__(self, Id, startTime):
        self.Id = Id  # String received from the SQS message
        self.startTime = datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")  # datetime received from the SQS message
        self.endTime = datetime.now()  # Will be replaced by the time it finishes
        self.subordersList = []  # List of suborders
        self.completed = False  # when completed, will changed to True
        self.totalSubs = 0  # Amount of suborders in order.

    def __iter__(self):
        return self

    def get_suborders(self):
        for suborder in self.subordersList:
            self.suborders.append(str(suborder))
        return self.suborders

    def __str__(self):
        return 'datetime: {0}, request_id: {1}, Order: {2}'.format(self.startTime, self.Id, self.get_suborders())


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
        return 'ID: {0}, Type: {1}, Meat: {2}, Quantity: {3}, Ingredients: {4}, To go: {5}'.format(self.Id, self.Type, self.meat, self.qty, self.ingr, self.to_go)


class Answer:
    stepsList = []

    def __init__(self, order):
        self.startTime = datetime.now()
        self.order = order
        self.endTime = datetime.now()
        self.steps = []  # List of steps that an order gets to be completed

    def get_steps(self):
        for step in self.steps:
            self.stepsList.append(str(step))
        return self.stepsList

    def __str__(self):
        return '{0}, answer: start_time: {1}, end_time: {2}, steps: {3}'.format(self.order.__str__(), self.startTime, self.endTime, self.get_steps())


class Steps:
    def __init__(self, step, state, action, Id):
        self.step = int(step)  # Number of steps that takes an order to be completed
        self.state = state  # Is it running or paused
        self.action = action
        self.Id = Id
        self.startTime = datetime.now()
        self.endTime = datetime.now()

    def __str__(self):
        return 'Step: {0}, State: {1}, Action: {2}, ID: {3}, StartTime: {4}, EndTime: {5}'.format(self.step, self.state, self.action, self.Id, self.startTime, self.endTime)
