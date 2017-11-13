from threading import Thread
import pandas as pd
from Taquero import *

# parallel threading
def Throw_Threads(queue_list,order_list):
    thread_list = []
    for t in queue_list:
        thread = Thread(target=taquero, args=(t,order_list), daemon=True)
        thread_list.append(thread)
        thread.start()
    for thread in thread_list:
        thread.join()
    raw_data = {"Order":[order.Id for order in order_list],
                "Time of completion": [(order.endTime-order.startTime).total_seconds() for order in order_list]}
    df = pd.DataFrame(raw_data, columns=['Order', 'Time of completion'])
    print(df)
    return df,order_list
