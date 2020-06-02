import telegram.ext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (MessageHandler, CallbackQueryHandler, Filters, ConversationHandler,Updater,CommandHandler)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)

from menu import (Menu, MenuGroup, MenuItem, MenuSerializer)
from order import (Order, OrderItem, OrderSerializer)

import orderstate

class OrderConversationManager(object):
    
    def __init__(self):
        self.menu = Menu()
        self.order = None
        self.menu_group_items = self.menu.get_menu_items()
        self.current_menu_item = None

    def start_order_command(self, update: telegram.Update, context: telegram.ext.CallbackContext):        
        self.state = orderstate.StartOrderState()
        self.order, self.current_menu_item = self.state.callback_query_handler(update, context, self.order, self.menu, self.current_menu_item)
        return self.state.conversation_state()

    def call_back_handle(self, update: telegram.Update, context: telegram.ext.CallbackContext):        
        self.order, self.current_menu_item = self.state.callback_query_handler(update, context, self.order, self.menu, self.current_menu_item)
        return self.state.conversation_state()
    