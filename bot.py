import telegram.ext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (MessageHandler, CallbackQueryHandler, Filters, ConversationHandler,Updater,CommandHandler)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import os.path
from os import path
import time
import ast
from menu import (Menu, MenuGroup, MenuItem, MenuSerializer)
from order import (Order, OrderItem, OrderSerializer)
from query_handlers import OperationOrderQueryHadler
from order_conversation_manager import OrderConversationManager
import orderstate

order_conversation_manager = OrderConversationManager()

# menu = Menu()
# order = None
# menu_group_items = menu.get_menu_items()
# current_menu_item = None

u = Updater('1175700257:AAF9HNQTnA1IOXAas1uShROLU2Jt4_OMwEo', use_context=True)
j = u.job_queue
crossIcon = u"\u274C"
checkIcon = u"\u2705" 

# def append_menu_group_keyboard(menu_group: MenuGroup, keyboard: list):
#     keyboard.append([InlineKeyboardButton(f'{menu_group.name}', callback_data=f'menu_group:{menu_group.id}')])

# def append_menu_item_keyboard(menu_item: MenuItem, order: Order, keyboard: list):
#     button_caption = f"{menu_item.price} :{menu_item.name}"
#     order_item = order.get_order_item(menu_item)
#     items_count = 0
#     if (order_item != None):
#         items_count = order_item.count

#     keyboard.append([InlineKeyboardButton(button_caption, callback_data=menu_item.id, resize_keyboard=True)])
#     keyboard.append([InlineKeyboardButton("+", callback_data=f'operation,{menu_item.id},+'),
#                     InlineKeyboardButton(f"{items_count}", callback_data=menu_item.id),
#                     InlineKeyboardButton("-", callback_data=f'operation,{menu_item.id},-')])    

# def append_menu_item_keyboard_for_order(order_item: OrderItem, order: Order, keyboard: list):
    
#     keyboard.append([InlineKeyboardButton(f"{order_item.name}", callback_data=order_item.id)])
#     keyboard.append([InlineKeyboardButton("+", callback_data=f'operation,{order_item.id},+'),
#             InlineKeyboardButton(f"{order_item.count}", callback_data=order_item.id),
#             InlineKeyboardButton("-", callback_data=f'operation,{order_item.id},-'),
#             InlineKeyboardButton(text=crossIcon, callback_data = f"operation,{order_item.id},delete")])

def start_command(update: telegram.Update, context: telegram.ext.CallbackContext):    
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a Camtek food orders bot, please use command /makeorder to order lunch!")    

#def make_order_command(update: telegram.Update, context: telegram.ext.CallbackContext):    
    
    # order = Order(update.message.from_user.name, context.chat_data)

    # keyboard = []
    # for m in menu_group_items:        
    #     append_menu_group_keyboard(m, keyboard)        

    # reply_markup = InlineKeyboardMarkup(keyboard, row_width = 1)
    # s = 'נא לבחור'
    # update.message.reply_text(text = s, reply_markup=reply_markup)
    
    #return conversation_state    

# def select_menu_item(update, context):

#     global order
#     global menu
#     global current_menu_item 

#     state = orderstate.SelectMenuItemState()
#     order, conversation_state = state.callback_query_handler(update, context, order, menu, current_menu_item)

#     return conversation_state

# def select_menu_item(update, context):
#     query = update.callback_query
#     query.answer()
    
#     global menu
#     global current_menu_item
#     global order

#     if (query.data == 'finish_order'):
#         query.edit_message_text(text = "הזמנה:", reply_markup=create_inline_keyboard_for_order(current_menu_item, order))        
#         return PLACE_ORDER

#     if (query.data.startswith("menu_group") == True):
#         arr = query.data.split(':')
#         current_menu_item = menu.get_menu_item(arr[1])
#     else:
#         operationOrderQueryHadler  = OperationOrderQueryHadler()
#         operationOrderQueryHadler.handle_query(query, menu, order)

#     query.edit_message_text(text = "נא לבחור", reply_markup= create_inline_keyboard_for_menu(current_menu_item, order))

# def create_inline_keyboard_for_menu(menu_group: MenuGroup, order: Order):
    
#     keyboard = []    
#     global current_menu_item

#     for m in menu.get_parent_menu_groups(current_menu_item):        
#         append_menu_group_keyboard(m, keyboard)        

#     for m in menu.get_menu_items(current_menu_item): 
#         if (isinstance(m, MenuGroup)):
#             append_menu_group_keyboard(m, keyboard)       
#         elif (isinstance(m, MenuItem)):
#             append_menu_item_keyboard(m, order, keyboard)       
        
#     if (len(order.get_order_items()) > 0):
#         keyboard.append([InlineKeyboardButton(f"{order.get_order_sum()} :סיים הזמנה", callback_data='finish_order')])

#     return InlineKeyboardMarkup(keyboard)  

# def create_inline_keyboard_for_order(menu_group: MenuGroup, order: Order):
    
#     keyboard = [] 
#     append_menu_group_keyboard(menu_group, keyboard)   
    
#     for order_item in order.get_order_items():        
#         append_menu_item_keyboard_for_order(order_item, order, keyboard)

#     keyboard.append([InlineKeyboardButton(f"{order.get_order_sum()} :תשלום", callback_data='pay')])
#     return InlineKeyboardMarkup(keyboard)

# def place_order(update, context):    
#     query = update.callback_query
#     query.answer()

#     global order
#     global current_menu_item

#     if (query.data == 'pay'):
#         keyboard = []
#         keyboard.append([InlineKeyboardButton(text=f'{checkIcon}סיים', callback_data = "ok"), InlineKeyboardButton(text=f'{crossIcon}לבטל', callback_data = "cancel")])
#         query.edit_message_text(text = "הזמנה", reply_markup=InlineKeyboardMarkup(keyboard))
#         return FINISH_ORDER
    
#     if (query.data.startswith("menu_group") == True):
#         arr = query.data.split(':')
#         current_menu_item = menu.get_menu_item(arr[1])
#         query.edit_message_text(text = "נא לבחור", reply_markup= create_inline_keyboard_for_menu(current_menu_item, order))        
#         return SELECT_MENU_ITEM
    
#     operationOrderQueryHadler = OperationOrderQueryHadler()

#     if (operationOrderQueryHadler.can_handle_query(query)):
#         operationOrderQueryHadler.handle_query(query, menu, order)
    
#     if (len(order.get_order_items()) > 0):    
#         query.edit_message_text(text = "הזמנה", reply_markup=create_inline_keyboard_for_order(current_menu_item, order))        
#     else:
#         query.edit_message_text(text = "נא לבחור", reply_markup= create_inline_keyboard_for_menu(current_menu_item, order))        
#         return SELECT_MENU_ITEM


# def finish_order(update, context):
    
    # query = update.callback_query
    # query.answer()

    # if (query.data != "ok"):
    #     query.edit_message_text('ההזמנה שלך בוטלה')
    #     return

    # global order

    # query.edit_message_text('תודה! ההזמנה שלך נשלחה')
    # orderSerializer = OrderSerializer()
    # orderSerializer.serialize(order, 'order.txt')
    
    # del order

    # return ConversationHandler.END

def callback_query_handle(update, context):
    conversation_state = order_conversation_manager.call_back_handle(update, context)

    if (conversation_state == orderstate.FINISH_ORDER):
        return ConversationHandler.END
    else:
        return conversation_state

def cancel(update, context):
    user = update.message.from_user    
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


start_command_handler = CommandHandler('start', start_command)    

conv_handler = ConversationHandler(
        entry_points=[CommandHandler('makeorder', order_conversation_manager.start_order_command)],

        states={            
            orderstate.SELECT_MENU_ITEM: [CallbackQueryHandler(callback_query_handle)],            
            orderstate.PLACE_ORDER: [CallbackQueryHandler(callback_query_handle)],
            orderstate.PAY_ORDER: [CallbackQueryHandler(callback_query_handle)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

u.dispatcher.add_handler(conv_handler)
u.dispatcher.add_handler(start_command_handler)

u.start_polling()