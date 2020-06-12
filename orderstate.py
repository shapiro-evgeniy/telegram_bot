from enum import Enum
from order import Order, OrderItem, OrderSerializer, OrdersRepository
from menu import Menu, MenuGroup, MenuItem
#from telegram import InlineKeyboardButton, InlineKeyboardMarkup
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

    # def append_menu_group_keyboard(self, menu_group: MenuGroup, keyboard: list):
    #     keyboard.append([InlineKeyboardButton(f'{menu_group.name}', callback_data=f'menu_group:{menu_group.id}')])

    # def append_menu_item_keyboard(self, menu_item: MenuItem, order: Order, keyboard: list):
    #     button_caption = f"{menu_item.price} :{menu_item.name}"
    #     order_item = order.get_order_item(menu_item)
    #     items_count = 0
    #     if (order_item != None):
    #         items_count = order_item.count

    #     keyboard.append([InlineKeyboardButton(button_caption, callback_data=menu_item.id, resize_keyboard=True)])
    #     keyboard.append([InlineKeyboardButton("-", callback_data=f'operation,{menu_item.id},-'),
    #                 InlineKeyboardButton(f"{items_count}", callback_data=menu_item.id),                    
    #                 InlineKeyboardButton("+", callback_data=f'operation,{menu_item.id},+')])    

    # def append_menu_item_keyboard_for_order(self, order_item: OrderItem, order: Order, keyboard: list):
        
    #     keyboard.append([InlineKeyboardButton(f"{order_item.name}", callback_data=order_item.id)])
    #     keyboard.append([InlineKeyboardButton("-", callback_data=f'operation,{order_item.id},-'),
    #             InlineKeyboardButton(f"{order_item.count}", callback_data=order_item.id),                
    #             InlineKeyboardButton("+", callback_data=f'operation,{order_item.id},+'),
    #             InlineKeyboardButton(text= self.crossIcon, callback_data = f"operation,{order_item.id},delete")])

    # def create_inline_keyboard_for_menu(self, menu_group: MenuGroup, menu: Menu, order: Order, current_menu_item: MenuGroup):
    
    #     keyboard = []    

    #     for m in menu.get_parent_menu_groups(current_menu_item):        
    #         self.append_menu_group_keyboard(m, keyboard)        

    #     for m in menu.get_menu_items(current_menu_item): 
    #         if (isinstance(m, MenuGroup)):
    #             self.append_menu_group_keyboard(m, keyboard)       
    #         elif (isinstance(m, MenuItem)):
    #             self.append_menu_item_keyboard(m, order, keyboard)       
            
    #     if (len(order.get_order_items()) > 0):
    #         keyboard.append([InlineKeyboardButton(f"{order.get_order_sum()} :סיים הזמנה", callback_data='finish_order')])

    #     return InlineKeyboardMarkup(keyboard)  

    
    # def create_inline_keyboard_for_order(self, menu_group: MenuGroup, order: Order):
    
    #     keyboard = [] 
    #     self.append_menu_group_keyboard(menu_group, keyboard)   
        
    #     for order_item in order.get_order_items():        
    #         self.append_menu_item_keyboard_for_order(order_item, order, keyboard)

    #     keyboard.append([InlineKeyboardButton(f"{order.get_order_sum()} :תשלום", callback_data='pay')])
    #     return InlineKeyboardMarkup(keyboard)

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
            orderConversationRepondent.respond_menu('הזמנה', {f'סיים': OrderConversationInputDataType.OK.name , f'לבטל': OrderConversationInputDataType.CANCEL.name})
            # keyboard = []
            # keyboard.append([InlineKeyboardButton(text=f'{self.checkIcon}סיים', callback_data = "ok"), InlineKeyboardButton(text=f'{self.crossIcon}לבטל', callback_data = "cancel")])
            # query.edit_message_text(text = "הזמנה", reply_markup=InlineKeyboardMarkup(keyboard))  
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
