from menu import MenuItem
import json

class OrderItem(object):
    def __init__(self, id: str, name: str, count: int, price: float):
        self.id = id
        self.name = name
        self.count = count
        self.price = price

class Order(object):    

    def __init__(self, user_id, chat_id, order_items = None):                
        self.user_id = user_id
        self.chat_id = chat_id

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
        with open(file_name, 'w') as outfile:    
            json.dump(order, default = lambda o: o.__dict__, fp = outfile, indent= 3)
    
    def unserialize(self, file_name: str) -> Order: 
        with open(file_name) as infile:    
            data = json.load(infile)

        order = Order(user_id= data['user_id'], chat_id=['chat_id'])

        for oi in data["order_items"]:
            order_item = OrderItem(**oi)
            order.add_or_update_order_item(order_item)

        return order        
