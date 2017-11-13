from queue import *

# Reads order from a list of dictionaries and place them in queues
def queues(data):
    # Queues are created for their later use.
    asada_queue = Queue()
    adobada_queue = Queue()
    others_queue = Queue()
    # In the time, we will be reading from a file named test.txt as if it was from an SQS message.
    for order in data:
        # print('\nNew Order', '\nID: ', order['request_id'], '\t', 'time: ',order['datetime'], '\n')
        # We read each dictionary.
        for suborder in order['orden']:  # sub-array of each order that will be addeded to a queue.
            tacos = Orden(suborder['part_id'], suborder['type'], suborder['meat'], suborder['quantity'],
                          suborder['ingredients'])
            # print(tacos)
            if tacos.meat == 'asada':
                asada_queue.put(tacos)
            elif tacos.meat == 'adobada':
                adobada_queue.put(tacos)
            else:
                others_queue.put(tacos)
    queue_list = [asada_queue, adobada_queue, others_queue]
    return queue_list
