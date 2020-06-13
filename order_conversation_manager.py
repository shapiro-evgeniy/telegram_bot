from abc import abstractmethod
from orderstate import OrderConversationInputData, OrderStateType

import telegram.ext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (MessageHandler, CallbackQueryHandler, Filters, ConversationHandler,Updater,CommandHandler)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)

from query_handlers import OrderConversationInputDataType
from menu import (Menu, MenuGroup, MenuItem, MenuSerializer)
from order import (Order, OrderItem, OrderSerializer)
from orderstate import (StartOrderState, SelectMenuItemState, OrderConversationInputData, OrderConversationRepondent)

class TelegramBotOrderConversationInputData(OrderConversationInputData):
    def __init__(self, update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
        self.update = update
        self.context = context
    def get_user_name(self)-> str:
        query = self.update.callback_query
        return query.from_user.name
    
    def get_type(self)->OrderConversationInputDataType:
        query = self.update.callback_query
        arr = query.data.split(':')
        return OrderConversationInputDataType[arr[0]]
    
    def get_content(self):
        query = self.update.callback_query
        arr = query.data.split(':')[1:]
        return arr

class TelegramBotOrderConversationRepondent(OrderConversationRepondent):

    crossIcon = u"\u274C"
    checkIcon = u"\u2705"

    def __init__(self, update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
        self.update = update
        self.context = context

    def __append_menu_group_keyboard(self, menu_group: MenuGroup, keyboard: list):
        keyboard.append([InlineKeyboardButton(f'{menu_group.name}', callback_data=f'{OrderConversationInputDataType.MENU_GROUP.name}:{menu_group.id}')])

    def __append_menu_item_keyboard(self, menu_item: MenuItem, order: Order, keyboard: list):
        button_caption = f"{menu_item.price} :{menu_item.name}"
        order_item = order.get_order_item(menu_item)
        items_count = 0
        if (order_item != None):
            items_count = order_item.count

        keyboard.append([InlineKeyboardButton(button_caption, callback_data=menu_item.id, resize_keyboard=True)])
        keyboard.append([InlineKeyboardButton("-", callback_data=f'{OrderConversationInputDataType.OPERATION.name}:{menu_item.id}:-'),
                    InlineKeyboardButton(f"{items_count}", callback_data=menu_item.id),                    
                    InlineKeyboardButton("+", callback_data=f'{OrderConversationInputDataType.OPERATION.name}:{menu_item.id}:+')])

    def __append_menu_item_keyboard_for_order(self, order_item: OrderItem, order: Order, keyboard: list):
        
        keyboard.append([InlineKeyboardButton(f"{order_item.name}", callback_data=order_item.id)])
        keyboard.append([InlineKeyboardButton("-", callback_data=f'{OrderConversationInputDataType.OPERATION.name}:{order_item.id}:-'),
                InlineKeyboardButton(f"{order_item.count}", callback_data=order_item.id),                
                InlineKeyboardButton("+", callback_data=f'{OrderConversationInputDataType.OPERATION.name}:{order_item.id}:+'),
                InlineKeyboardButton(text= self.crossIcon, callback_data = f"{OrderConversationInputDataType.OPERATION.name}:{order_item.id}:delete")])

    def respond_for_order_sub_menu(self, current_menu_item: MenuGroup, menu: Menu, order: Order):

        keyboard = []    

        for m in menu.get_parent_menu_groups(current_menu_item):        
            self.__append_menu_group_keyboard(m, keyboard)        

        for m in menu.get_menu_items(current_menu_item): 
            if (isinstance(m, MenuGroup)):
                self.__append_menu_group_keyboard(m, keyboard)       
            elif (isinstance(m, MenuItem)):
                self.__append_menu_item_keyboard(m, order, keyboard)       
                       
        if (len(order.get_order_items()) > 0):
            keyboard.append([InlineKeyboardButton(f"{order.get_order_sum()} :סיים הזמנה", callback_data=f'{OrderConversationInputDataType.FINISH_ORDER.name}')])

        reply_merkup = InlineKeyboardMarkup(keyboard)
        
        query = self.update.callback_query
        query.answer()

        query.edit_message_text(text = "נא לבחור", reply_markup= reply_merkup)

    def respond_for_order_menu(self, menu: Menu, order: Order):

        keyboard = []
        for m in menu.get_menu_items():        
            self.__append_menu_group_keyboard(m, keyboard)        
        
        reply_markup = InlineKeyboardMarkup(keyboard, row_width = 1)
        
        query = self.update.callback_query
        query.answer()

        query.edit_message_text(text = "נא לבחור", reply_markup=reply_markup)

    def respond_for_order(self, menu_group: MenuGroup, order: Order):
        
        keyboard = [] 
        self.__append_menu_group_keyboard(menu_group, keyboard)   
        
        for order_item in order.get_order_items():        
            self.__append_menu_item_keyboard_for_order(order_item, order, keyboard)

        keyboard.append([InlineKeyboardButton(f"{order.get_order_sum()} :תשלום", callback_data=f'{OrderConversationInputDataType.PAY_ORDER.name}')])
        reply_merkup = InlineKeyboardMarkup(keyboard)

        query = self.update.callback_query
        #query.answer()

        query.edit_message_text(text = "הזמנה:", reply_markup= reply_merkup)  

    def respond_simple_message(self, message: str):
        query = self.update.callback_query
        query.answer()
        query.edit_message_text(message)

    def respond_menu(self, header:str, menu: dict):
        
        query = self.update.callback_query
        query.answer()
        
        keyboard = []
        for (k,v) in menu.items(): 
            keyboard.append([InlineKeyboardButton(f'{k}', callback_data=f'{v}')])

        # for (k,v) in menu.items():            
        #      keyboard.append([InlineKeyboardButton(k, callback_data = v)])
        reply_merkup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text(text = header, reply_markup=reply_merkup)  

class OrderConversationManager(object):
    
    def __init__(self):
        self.menu = Menu()
        self.order = Order('')
        self.menu_group_items = self.menu.get_menu_items()
        self.current_menu_item = None

    def start_order_command(self, orderConversationInputData: OrderConversationInputData, orderConversationRepondent: OrderConversationRepondent) -> OrderStateType:        
        self.state = StartOrderState()
        self.order, self.current_menu_item = self.state.callback_query_handler(orderConversationInputData, orderConversationRepondent, self.order, self.menu, self.current_menu_item)
        return self.state.conversation_state()

    def call_back_handle(self, orderConversationInputData: OrderConversationInputData, orderConversationRepondent: OrderConversationRepondent) -> OrderStateType:        
        self.order, self.current_menu_item = self.state.callback_query_handler(orderConversationInputData, orderConversationRepondent, self.order, self.menu, self.current_menu_item)
        return self.state.conversation_state()

    def set_order(self, orderConversationInputData: OrderConversationInputData, orderConversationRepondent: OrderConversationRepondent, order: Order)-> OrderStateType:
        self.state = SelectMenuItemState()
        self.order = order
        self.current_menu_item = self.menu.get_menu_items()[0]
        self.order, self.current_menu_item = self.state.callback_query_handler(orderConversationInputData, orderConversationRepondent, self.order, self.menu, self.current_menu_item)
        return self.state.conversation_state()
    