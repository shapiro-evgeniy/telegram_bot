import telegram.ext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (MessageHandler, CallbackQueryHandler, Filters, ConversationHandler,Updater,CommandHandler)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from menu import (Menu, MenuGroup, MenuItem, MenuSerializer)
from order import (Order, OrderItem, OrderSerializer, OrdersRepository)
from query_handlers import OperationOrderQueryHadler, OrderConversationInputDataType
from order_conversation_manager import OrderConversationManager, TelegramBotOrderConversationInputData, TelegramBotOrderConversationRepondent
import orderstate

order_conversation_manager = OrderConversationManager()

u = Updater('1175700257:AAF9HNQTnA1IOXAas1uShROLU2Jt4_OMwEo', use_context=True)
j = u.job_queue
crossIcon = u"\u274C"
checkIcon = u"\u2705" 

START_CONVERSATION, SELECT_EXISTSING_ORDER = range(2)

def start_command(update: telegram.Update, context: telegram.ext.CallbackContext ):  
    return start_command_internal(update, reply_to_message)

def start_command_internal(update: telegram.Update, reply_func):
    
    keyboard = [
        [InlineKeyboardButton('ההזמנות שלי', callback_data='orders'),
         InlineKeyboardButton('חנות קפה', callback_data='start_order')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_func(update, '!אני בוט של החנות קפה. בעזרתי אפשר להזמין את הקפה', reply_markup)

    return START_CONVERSATION

def reply_to_message(update: telegram.Update, answer: str, reply_markup):
    update.message.reply_text(text=answer, reply_markup = reply_markup)

def reply_to_query(update: telegram.Update, answer: str, reply_markup):
    query = update.callback_query
    query.answer()

    query.edit_message_text(text = answer, reply_markup=reply_markup)

def start_conversation_callback_query_handle(update: telegram.Update, context: telegram.ext.CallbackContext):
    
    query = update.callback_query
    query.answer()
    
    orderConversationInputData = TelegramBotOrderConversationInputData(update, context)
    orderConversationRepondent = TelegramBotOrderConversationRepondent(update, context)

    if query.data == 'start_order':        
        return order_conversation_manager.start_order_command(orderConversationInputData, orderConversationRepondent)     

    keyboard = []    
    orders_repository = OrdersRepository(OrderSerializer())
    user_orders = orders_repository.get_order_names_for_user(query.from_user.name)

    if not user_orders or len(user_orders) == 0:
        return start_command_internal(update, reply_to_query)

    for order in user_orders:     
        keyboard.append([InlineKeyboardButton(f"{order}", callback_data=order)])
    
    reply_to_query(update, 'נא לבחור', reply_markup=InlineKeyboardMarkup(keyboard, row_width = 1))
    
    return SELECT_EXISTSING_ORDER        

def select_existing_order_callback_query_handle(update: telegram.Update, context: telegram.ext.CallbackContext):
    
    query = update.callback_query
    query.answer()

    orders_repository = OrdersRepository(OrderSerializer())
    order = orders_repository.get_order(query.from_user.name, query.data)

    query.data = OrderConversationInputDataType.FINISH_ORDER.name

    orderConversationInputData = TelegramBotOrderConversationInputData(update, context)
    orderConversationRepondent = TelegramBotOrderConversationRepondent(update, context)

    return order_conversation_manager.set_order(orderConversationInputData, orderConversationRepondent, order)

def order_callback_query_handle(update, context) -> int:     
    
    orderConversationInputData = TelegramBotOrderConversationInputData(update, context)
    orderConversationRepondent = TelegramBotOrderConversationRepondent(update, context)

    conversation_state = order_conversation_manager.call_back_handle(orderConversationInputData, orderConversationRepondent)

    if (conversation_state == orderstate.OrderStateType.FINISH_ORDER):
        start_command_internal(update, reply_to_query)
        return START_CONVERSATION
    else:
        return conversation_state

def cancel(update, context):
    user = update.message.from_user    
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

conv_handler = ConversationHandler(        
        entry_points=[CommandHandler('start', start_command)],

        states={  
            START_CONVERSATION: [CallbackQueryHandler(start_conversation_callback_query_handle)],                                  
            orderstate.OrderStateType.START_ORDER: [CallbackQueryHandler(order_callback_query_handle)],            
            orderstate.OrderStateType.SELECT_MENU_ITEM: [CallbackQueryHandler(order_callback_query_handle)],            
            orderstate.OrderStateType.PLACE_ORDER: [CallbackQueryHandler(order_callback_query_handle)],
            orderstate.OrderStateType.PAY_ORDER: [CallbackQueryHandler(order_callback_query_handle)],
            SELECT_EXISTSING_ORDER: [CallbackQueryHandler(select_existing_order_callback_query_handle)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

u.dispatcher.add_handler(conv_handler)

u.start_polling()