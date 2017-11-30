from datetime import datetime


class Order(object):
    suborders = []
    stepsList = []

    def __init__(self, Id, startTime):
        self.Id = Id  # String received from the SQS message
        #self.startTime = datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")  # datetime received from the SQS message
        self.startTime = datetime.now()
        self.endTime = datetime.now()  # Will be replaced by the time it finishes
        self.subordersList = []  # List of suborders
        self.completed = False  # when completed, will changed to True
        self.totalSubs = 0  # Amount of suborders in order.

    def __iter__(self):
        return self

    def get_suborders(self):
        self.suborders.clear()
        for suborder in self.subordersList:
            self.suborders.append(suborder.__dict__())
        return self.suborders

    def get_steps(self):
        self.stepsList.clear()
        for suborder in self.subordersList:
            stepCount = 0  # Counts all the steps that a suborder went through
            for step in suborder.steps:
                stepCount += 1
                step.step = stepCount
                self.stepsList.append(step.__dict__())
        return self.stepsList


class Suborder(object):
    def __init__(self, Id, Type, meat, qty, ingr):
        self.Id = Id  # String received from the SQS message
        self.startTime = datetime.now()
        self.endTime = datetime.now()  # Will be replaced by the time it finishes
        self.Type = Type  # Type of order, like quesadilla, taco, mulita, etc.
        self.meat = meat  # Type of meat for the order
        self.qty = int(qty)  # Quantity of tacos ordered
        self.tacosToMake = int(qty)  # Used to know how many tacos have been made, this will go down to zero
        self.ingr = ingr  # Ingredients
        self.to_go = False  # If it to go it will change
        self.waitCycle = 0  # Time waiting to be processed, used as priority condition
        self.completed = False  # When completed, will change to True
        self.steps = []  # List of steps that an order gets to be completed

    def __dict__(self):
        suborder = {'ID': self.Id, 'Type': self.Type, 'Meat': self.meat, 'Quantity': self.qty, 'Ingredients': self.ingr, 'To_go': self.to_go}
        return suborder


class Answer(object):
    def __init__(self, order):
        self.order = order

    def __dict__(self):
        suborders = self.order.get_suborders()
        answer = {'datetime': str(self.order.startTime), 'request_id': self.order.Id, 'order': suborders,
                  'answer': {'start_time': str(self.order.startTime), 'end_time': str(self.order.endTime), 'steps': self.order.get_steps()}}
        return answer

    def __iter__(self):
        return self


class Steps(object):
    def __init__(self, state, action, Id):
        self.step = int()  # Number of steps that takes an order to be completed
        self.state = state  # Is it running or paused
        self.action = action
        self.Id = Id
        self.startTime = datetime.now()
        self.endTime = datetime.now()

    def __dict__(self):
        step = {'Step': self.step, 'State': self.state, 'Action': self.action, 'part_id': self.Id,'StartTime': str(self.startTime), 'EndTime': str(self.endTime)}
        return step
