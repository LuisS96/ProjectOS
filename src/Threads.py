from threading import Thread
import pandas as pd
from Taquero import *

# parallel threading
def Throw_Threads(queue_list):
    thread_list = []
    for t in queue_list:
        thread = Thread(target=taquero, args=(t,), daemon=True)
        thread_list.append(thread)
        thread.start()
    for thread in thread_list:
        thread.join()
    raw_data = {'Queues': ['Asada', 'Adobada', 'Otros'],
                'Quantity': [queue_list[0].qsize(), queue_list[1].qsize(), queue_list[2].qsize()]}
    df = pd.DataFrame(raw_data, columns=['Queues', 'Quantity'])
    print(df)
    return df
