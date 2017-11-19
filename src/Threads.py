from threading import Thread
from Process import *

def threads(queues, answersList):  # Parallel threading
    threadsList = []
    for queue in queues:
        thread = Thread(target=taquero, args=(queue, answersList), daemon=True)
        threadsList.append(thread)
        thread.start()
    for thread in threadsList:
        thread.join()
