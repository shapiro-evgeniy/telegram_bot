from menu import MenuItem
import json
import os

class OrderItem(object):
    def __init__(self, id: str, name: str, count: int, price: float):
        self.id = id
        self.name = name
        self.count = count
        self.price = price

class Order(object):    

    def __init__(self, user_id, order_items: list = None):                
        self.user_id = user_id        

        if order_items is None:
            self.order_items = []
        else:
            self.order_items = order_items

    def add_or_update_order_item(self, new_order_item: OrderItem):
        order_item = next((item for item in self.order_items if item.id == new_order_item.id), None)

        if order_item != None:
            order_item.count = new_order_item.count
        else:
            self.order_items.append(new_order_item)  

    def get_order_item(self, menu_item: MenuItem):
        return next((item for item in self.order_items if item.id == menu_item.id), None)

    def get_order_item_by_id(self, order_item_id):
        return next((item for item in self.order_items if item.id == order_item_id), None)

    def get_order_items(self):
        return self.order_items
    
    def remove_order_item(self, order_item_id):
        self.order_items.remove(next((item for item in self.order_items if item.id == order_item_id), None))    

    def get_order_sum(self):
        sum = 0
        for order_item in self.order_items:
            sum += order_item.count * order_item.price
        return sum

class OrderSerializer():
    def serialize(self, order: Order, file_name: str):
        dirname = os.path.dirname(file_name)
        if dirname != '' and not os.path.exists(dirname):    
            os.makedirs(os.path.dirname(file_name))

        with open(file_name, 'w') as outfile:    
            json.dump(order, default = lambda o: o.__dict__, fp = outfile, indent= 3)
    
    def unserialize(self, file_name: str) -> Order: 
        with open(file_name) as infile:    
            data = json.load(infile)

        order = Order(user_id= data['user_id'])

        for oi in data["order_items"]: 
            order_item = OrderItem(**oi)
            order.add_or_update_order_item(order_item)

        return order 

class OrdersRepository():

    def __init__(self, order_serializer: OrderSerializer) -> None:
        self.order_serializer = order_serializer

    def get_order_names_for_user(self, user_id: str) -> list:

        if not user_id or user_id.strip() == False:
            return []

        path = f'orders\\{user_id}'
        orders = []
        for root, dir, files in os.walk(path):
            for file in files:
                filename, file_extension = os.path.splitext(file)
                if file_extension == '.json':
                    orders.append(filename)

        return orders

    def save_order_for_user(self, order: Order):
        if not order.user_id or order.user_id.strip() == False:
            raise ValueError('Invalid order')

        file_name = f'orders\\{order.user_id}\\Order {order.get_order_sum()}.json'
        self.order_serializer.serialize(order, file_name)

    def get_order(self, user_id:str, order_id:str) -> Order:
        file_name = f'orders\\{user_id}\\{order_id}.json'

        order = self.order_serializer.unserialize(file_name)
        return order

# os = OrderSerializer()
# os1 = OrdersRepository(os)
# my_order = os1.get_order('Evgeny Shapiro', 'Order 75')
# print(my_order)

# orders = os1.get_order_names_for_user('User_123')
# orders = os1.get_order_names_for_user('User_3')


# order = Order('my_user', '1123123123')
# order_item = OrderItem('wqeqw', 'order_item1', 3, 2.5)
# order.add_or_update_order_item(order_item)
# order_item = OrderItem('gfdgdfg', 'order_item2', 5, 3.5)
# order.add_or_update_order_item(order_item)

# os1.save_order_for_user(order)
# orders = os1.get_order_names_for_user(order.user_id)
# print(orders)