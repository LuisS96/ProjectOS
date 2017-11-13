from _threading import Thread
import queue


#parallel threading
def Throw_Threads(asada_queue, adobada_queue, others_queue):

    queue_list = [asada_queue, adobada_queue, others_queue]
    thread_list = []

    for t in queue_list:
        thread = Thread(target=taquero, args=(t,), daemon=True)
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()

    raw_data = {'Queues': ['Asada', 'Adobada', 'Otros'],
                'Quantity': [asada_queue.qsize(), adobada_queue.qsize(), others_queue.qsize()]}
    df = pd.DataFrame(raw_data, columns=['Queues', 'Quantity'])
    print(df)
    return df
