from order import Order, OrderItem
from menu import Menu

class QueryHadlerInterface:
    def can_handle_query(self, query) -> bool:
        pass

    def handle_query(self, query, menu: Menu, order: Order):
        pass

class FinishOrderQueryHadler(QueryHadlerInterface):
    def can_handle_query(self, query) -> bool:
        return query.data == 'finish_order'

    def handle_query(self, query, menu: Menu, order: Order):
        pass

class OperationOrderQueryHadler(QueryHadlerInterface):

    def __get_order_item_count(self, x, order_item: OrderItem):
        return {
            '+': order_item.count + 1,
            '-': order_item.count - 1,
            'delete': 0
        }.get(x,x)

    def can_handle_query(self, query) -> bool:
        return query.data.startswith("operation")

    def handle_query(self, query, menu: Menu, order: Order):
        arr = query.data.split(',')
        order_item = order.get_order_item_by_id(arr[1])        
    
        if (order_item == None):
            menu_item = menu.get_menu_item(arr[1])
            order_item = OrderItem(menu_item.id, menu_item.name, 0, menu_item.price)

        order_item.count = self.__get_order_item_count(arr[2], order_item)
        
        if (order_item.count > 0):
            order.add_or_update_order_item(order_item)
        else:
            order.remove_order_item(order_item.id)

class MenuGroupQueryHadler(QueryHadlerInterface):
    def can_handle_query(self, query) -> bool:
        return query.data.startswith("menu_group")

    def handle_query(self, query, menu: Menu, order: Order):
        pass
    