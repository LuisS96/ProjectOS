from Charts import *
from Queues import *
from class_order import *
from read_json_file import *
from Taquero import *
from Threads import *

#Read file
file = "Order.json"
order = read_order(file)

#Insert each order in queues according to type of meat to be used by a taquero
queue = queues(order)

#For each taquero a thread is created, and will prepared the order of tacos
taquero = Throw_Threads(queue)

#Create the charts according to the statistics of a taquero
charts(taquero)