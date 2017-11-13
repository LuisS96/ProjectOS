from queue import *


def Switch(wait_queue,current,next):
    current.wcycle += 1
    wait_queue.put(current)
    print('ID: ', current.Id, '\tStatus: Pause...', )
    current = next
    print('ID: ', current.Id, '\tStatus: Resume...', )
    next = wait_queue.get()
    return current,next


def taquero(tacos_queue):
    cycle = 2
    wait_queue = Queue()
    current = tacos_queue.get()
    while tacos_queue.empty() is False:
        print('ID: ', current.Id, '\tStatus: Starting your suborder of tacos...', )
        time.sleep(1)
        next = tacos_queue.get()
        current.qty -= cycle
        #According to size of order it forces to complete an order instead of increasing an overhead
        if current.qty == 1:
            current.qty -= cycle
        #While for switch
        while current.qty > 0:
            current,next = Switch(wait_queue,current,next)
            print('qty: ',current.qty,'id: ',current.Id)
            #Bonus cycles for huge orders
            if current.wcycle >= 8:
                current.qty -= cycle*4
            #Bonus cycles for big orders
            elif current.wcycle >= 6:
                current.qty -= cycle*3
            #Bonus cycles for medium orders
            elif current.wcycle >= 2:
                current.qty -= cycle*2
            #Small orders do not have bonus cycles
            else:
                current.qty -= cycle
            if current.qty == 1:
                current.qty -= cycle
        print('ID: ', current.Id, '\tStatus: Suborder finished', )
        # print('\n',current)
        current = next
    #Finishing the last order
    while next.qty > 0:
        current = next
        current.qty -= cycle
    print('ID: ', current.Id, '\tStatus: Resume...', )
    print('ID: ', current.Id, '\tStatus: Suborder finished', )
