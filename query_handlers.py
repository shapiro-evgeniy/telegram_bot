from order import Order, OrderItem
from menu import Menu
from abc import abstractmethod
from enum import Enum

class OrderConversationInputDataType(Enum):
    OPERATION = 0
    MENU_GROUP = 1
    FINISH_ORDER = 2
    PAY_ORDER = 3
    OK = 4
    CANCEL = 5

class OrderConversationInputData(object):
    @abstractmethod
    def get_user_name(self)-> str:
        pass

    @abstractmethod
    def get_type(self)->OrderConversationInputDataType:
        pass

    @abstractmethod
    def get_content(self):
        pass

class QueryHadlerInterface:
    @abstractmethod
    def can_handle_query(self, query) -> bool:
        pass
    
    @abstractmethod
    def handle_query(self, query, menu: Menu, order: Order):
        pass

class OperationOrderQueryHadler(QueryHadlerInterface):

    def __get_order_item_count(self, x, order_item: OrderItem):
        return {
            '+': order_item.count + 1,
            '-': order_item.count - 1,
            'delete': 0
        }.get(x,x)

    def can_handle_query(self, orderConversationInputData: OrderConversationInputData) -> bool:
        return orderConversationInputData.get_type() == OrderConversationInputDataType.OPERATION

    def handle_query(self, orderConversationInputData: OrderConversationInputData, menu: Menu, order: Order):        
        
        order_item_id = orderConversationInputData.get_content()[0]
        order_item = order.get_order_item_by_id(order_item_id)        
    
        if (order_item == None):
            menu_item = menu.get_menu_item(order_item_id)
            order_item = OrderItem(menu_item.id, menu_item.name, 0, menu_item.price)

        order_item.count = self.__get_order_item_count(orderConversationInputData.get_content()[1], order_item)
        
        if (order_item.count > 0):
            order.add_or_update_order_item(order_item)
        else:
            order.remove_order_item(order_item.id)