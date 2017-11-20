from threading import Thread
from Process import *


def threads(queues, answersList, ingrQty):  # Parallel threading
    threadsList = []
    for pos in range(len(queues)):
        thread = Thread(target=taquero, args=(queues[pos], answersList, ingrQty[pos]), daemon=True)
        threadsList.append(thread)
        thread.start()
    for thread in threadsList:
        thread.join()
