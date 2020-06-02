import time
import os.path
from os import path

def get_orders_file_name():    
    return 'orders_' + time.strftime("%Y%m%d") + '.txt'

def get_orders():
    orders = []

    if path.exists(get_orders_file_name()) != True:
        print('File not exists')
        return orders   
    
    file = open(get_orders_file_name(), 'r')
    f = file.readlines()

    for line in f:
        print(line.strip('\n'))
        orders.append(line.strip('\n'))

    file.close()
    return orders

def save_order(order):
    file = open(get_orders_file_name(), 'a+')
    file.seek(0)
    data = file.read(1)
    print(len(data))
    if len(data) > 0 :
        file.write("\n")
    file.write(order)    
    file.close()  

save_order('MyOrder:Salat1')
save_order('MyOrder:Salat1')
save_order('MyOrder:Salat1')
print(get_orders())