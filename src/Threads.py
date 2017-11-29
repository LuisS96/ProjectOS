from threading import Thread
from Process import *


def threads(queues, answersList, ingrQty,threadPermits):  # Parallel threading
    threadsList = []
    for pos in range(len(queues)):
        if threadPermits[pos] == 1:
            thread = Thread(target=taquero, args=(queues[pos], answersList, ingrQty[pos]), daemon=True)
            threadsList.append(thread)
            thread.start()
            threadPermits[pos] = 0
    # for thread in threadsList:
    #     thread.join()
