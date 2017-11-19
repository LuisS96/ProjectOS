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
            self.suborders.append(suborder.__dict__())
        return self.suborders


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

    def __dict__(self):
        suborder = {'ID': self.Id, 'Type': self.Type, 'Meat': self.meat, 'Quantity': self.qty, 'Ingredients': self.ingr, 'To_go': self.to_go}
        return suborder


class Answer:
    stepsList = []

    def __init__(self, order):
        self.startTime = datetime.now()
        self.order = order
        self.endTime = datetime.now()
        self.steps = []  # List of steps that an order gets to be completed

    def get_steps(self):
        for step in self.steps:
            self.stepsList.append(step.__dict__())
        return self.stepsList

    def __dict__(self):
        suborders = self.order.get_suborders()
        answer = {'datetime': str(self.order.startTime), 'request_id': self.order.Id, 'order': suborders,
                  'answer': {'start_time': str(self.startTime), 'end_time': str(self.endTime), 'steps': self.get_steps()}}
        return answer

    def __iter__(self):
        return self


class Steps:
    def __init__(self, step, state, action, Id):
        self.step = int(step)  # Number of steps that takes an order to be completed
        self.state = state  # Is it running or paused
        self.action = action
        self.Id = Id
        self.startTime = datetime.now()
        self.endTime = datetime.now()

    def __dict__(self):
        step = {'Step': self.step, 'State': self.state, 'Action': self.action, 'part_id': self.Id,'StartTime': str(self.startTime), 'EndTime': str(self.endTime)}
        return step