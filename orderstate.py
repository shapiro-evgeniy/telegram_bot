from enum import Enum
from order import Order, OrderItem, OrderSerializer, OrdersRepository
from menu import Menu, MenuGroup, MenuItem
from query_handlers import OperationOrderQueryHadler, OrderConversationInputData, OrderConversationInputDataType
from abc import abstractmethod

class OrderStateType(Enum):
    START_ORDER = 100
    SELECT_MENU_ITEM = 200
    PLACE_ORDER = 300
    PAY_ORDER = 400
    FINISH_ORDER = 500

class OrderConversationRepondent(object):

    @abstractmethod
    def respond_menu(self, header:str, menu: dict):
        pass

    @abstractmethod
    def respond_for_order_menu(self, menu: Menu, order: Order):
        pass

    @abstractmethod
    def respond_for_order_sub_menu(self, current_menu_item: MenuGroup, menu: Menu, order: Order):
        pass

    @abstractmethod
    def respond_for_order(self, menu_group: MenuGroup, order: Order):
        pass

    @abstractmethod
    def respond_simple_message(self, message: str):
        pass

class OrderState(object):

    crossIcon = u"\u274C"
    checkIcon = u"\u2705" 

    @abstractmethod
    def conversation_state(self) -> OrderStateType:
        pass

    @abstractmethod    
    def callback_query_handler(self, orderConversationInputData: OrderConversationInputData, orderConversationRepondent: OrderConversationRepondent, order: Order, menu: Menu, current_menu_item: MenuGroup):
        pass    

class StartOrderState(OrderState):
    def callback_query_handler(self, orderConversationInputData: OrderConversationInputData, orderConversationRepondent: OrderConversationRepondent, order: Order, menu: Menu, current_menu_item: MenuGroup):
        
        order = Order(orderConversationInputData.get_user_name())
        orderConversationRepondent.respond_for_order_menu(menu, order)

        self.__class__ = SelectMenuItemState
    
        return order, current_menu_item

    def conversation_state(self) -> OrderStateType:
        return OrderStateType.START_ORDER   

class SelectMenuItemState(OrderState):

    def callback_query_handler(self, orderConversationInputData: OrderConversationInputData, orderConversationRepondent: OrderConversationRepondent, order: Order, menu: Menu, current_menu_item: MenuGroup):
        
        if (orderConversationInputData.get_type() == OrderConversationInputDataType.FINISH_ORDER):
            orderConversationRepondent.respond_for_order(current_menu_item, order)
            self.__class__ = PlaceOrderState
            return order, current_menu_item

        if (orderConversationInputData.get_type() == OrderConversationInputDataType.MENU_GROUP):
            menu_item_id = orderConversationInputData.get_content()[0]
            current_menu_item = menu.get_menu_item(menu_item_id)
        else:
            operationOrderQueryHadler  = OperationOrderQueryHadler()
            operationOrderQueryHadler.handle_query(orderConversationInputData, menu, order)

        orderConversationRepondent.respond_for_order_sub_menu(current_menu_item, menu, order)        
        return order, current_menu_item

    def conversation_state(self) -> OrderStateType:
        return OrderStateType.SELECT_MENU_ITEM

class PlaceOrderState(OrderState):

    def callback_query_handler(self, orderConversationInputData: OrderConversationInputData, orderConversationRepondent: OrderConversationRepondent, order: Order, menu: Menu, current_menu_item: MenuGroup):

        if (orderConversationInputData.get_type() == OrderConversationInputDataType.PAY_ORDER):
            orderConversationRepondent.respond_menu('הזמנה', {f'{OrderState.checkIcon}סיים': OrderConversationInputDataType.OK.name , f'{OrderState.crossIcon}לבטל': OrderConversationInputDataType.CANCEL.name})
            self.__class__ = PayOrderState           
            return order, current_menu_item
        
        if (orderConversationInputData.get_type() == OrderConversationInputDataType.MENU_GROUP):
            menu_item_id = orderConversationInputData.get_content()[0]
            current_menu_item = menu.get_menu_item(menu_item_id)
            orderConversationRepondent.respond_for_order_sub_menu(current_menu_item, menu, order)
            self.__class__ = SelectMenuItemState 
            return order, current_menu_item
        
        operationOrderQueryHadler = OperationOrderQueryHadler()

        if (operationOrderQueryHadler.can_handle_query(orderConversationInputData)):
            operationOrderQueryHadler.handle_query(orderConversationInputData, menu, order)
        
        if (len(order.get_order_items()) > 0):                
            orderConversationRepondent.respond_for_order(current_menu_item, order)
        else:
            orderConversationRepondent.respond_for_order_sub_menu(current_menu_item, menu, order)
            self.__class__ = SelectMenuItemState 
        
        return order, current_menu_item

    def conversation_state(self) -> OrderStateType:
        return OrderStateType.PLACE_ORDER

class PayOrderState(OrderState):
    def callback_query_handler(self, orderConversationInputData: OrderConversationInputData, orderConversationRepondent: OrderConversationRepondent, order: Order, menu: Menu, current_menu_item: MenuGroup):
        
        if (orderConversationInputData.get_type() == OrderConversationInputDataType.CANCEL):
            orderConversationRepondent.respond_simple_message('ההזמנה שלך בוטלה')
        else:
            orderConversationRepondent.respond_simple_message('תודה! ההזמנה שלך נשלחה')
            ordersRepository = OrdersRepository(OrderSerializer())
            ordersRepository.save_order_for_user(order)

        self.__class__ = FinishOrderState 

        del order
        del current_menu_item

        return None, None 

    def conversation_state(self) -> OrderStateType:
        return OrderStateType.PAY_ORDER

class FinishOrderState(OrderState):
    def callback_query_handler(self, orderConversationInputData: OrderConversationInputData, orderConversationRepondent: OrderConversationRepondent, order: Order, menu: Menu, current_menu_item: MenuGroup):
        pass
    def conversation_state(self) -> OrderStateType:
        return OrderStateType.FINISH_ORDER
