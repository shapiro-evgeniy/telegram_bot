from order import Order, OrderItem, OrderSerializer
from menu import Menu, MenuGroup, MenuItem
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from query_handlers import OperationOrderQueryHadler

SELECT_MENU_ITEM, PLACE_ORDER, PAY_ORDER, FINISH_ORDER = range(4)

class OrderState(object):

    crossIcon = u"\u274C"
    checkIcon = u"\u2705" 

    def conversation_state(self):
        pass

    def callback_query_handler(self, update, context, order: Order, menu: Menu, current_menu_item: MenuGroup):
        pass

    def append_menu_group_keyboard(self, menu_group: MenuGroup, keyboard: list):
        keyboard.append([InlineKeyboardButton(f'{menu_group.name}', callback_data=f'menu_group:{menu_group.id}')])

    def append_menu_item_keyboard(self, menu_item: MenuItem, order: Order, keyboard: list):
        button_caption = f"{menu_item.price} :{menu_item.name}"
        order_item = order.get_order_item(menu_item)
        items_count = 0
        if (order_item != None):
            items_count = order_item.count

        keyboard.append([InlineKeyboardButton(button_caption, callback_data=menu_item.id, resize_keyboard=True)])
        keyboard.append([InlineKeyboardButton("-", callback_data=f'operation,{menu_item.id},-'),
                    InlineKeyboardButton(f"{items_count}", callback_data=menu_item.id),                    
                    InlineKeyboardButton("+", callback_data=f'operation,{menu_item.id},+')])    

    def append_menu_item_keyboard_for_order(self, order_item: OrderItem, order: Order, keyboard: list):
        
        keyboard.append([InlineKeyboardButton(f"{order_item.name}", callback_data=order_item.id)])
        keyboard.append([InlineKeyboardButton("-", callback_data=f'operation,{order_item.id},-'),
                InlineKeyboardButton(f"{order_item.count}", callback_data=order_item.id),                
                InlineKeyboardButton("+", callback_data=f'operation,{order_item.id},+'),
                InlineKeyboardButton(text= self.crossIcon, callback_data = f"operation,{order_item.id},delete")])

    def create_inline_keyboard_for_menu(self, menu_group: MenuGroup, menu: Menu, order: Order, current_menu_item: MenuGroup):
    
        keyboard = []    

        for m in menu.get_parent_menu_groups(current_menu_item):        
            self.append_menu_group_keyboard(m, keyboard)        

        for m in menu.get_menu_items(current_menu_item): 
            if (isinstance(m, MenuGroup)):
                self.append_menu_group_keyboard(m, keyboard)       
            elif (isinstance(m, MenuItem)):
                self.append_menu_item_keyboard(m, order, keyboard)       
            
        if (len(order.get_order_items()) > 0):
            keyboard.append([InlineKeyboardButton(f"{order.get_order_sum()} :סיים הזמנה", callback_data='finish_order')])

        return InlineKeyboardMarkup(keyboard)  

    
    def create_inline_keyboard_for_order(self, menu_group: MenuGroup, order: Order):
    
        keyboard = [] 
        self.append_menu_group_keyboard(menu_group, keyboard)   
        
        for order_item in order.get_order_items():        
            self.append_menu_item_keyboard_for_order(order_item, order, keyboard)

        keyboard.append([InlineKeyboardButton(f"{order.get_order_sum()} :תשלום", callback_data='pay')])
        return InlineKeyboardMarkup(keyboard)

class StartOrderState(OrderState):
    def callback_query_handler(self, update, context, order: Order, menu: Menu, current_menu_item: MenuGroup):
        order = Order(update.message.from_user.name, context.chat_data)

        keyboard = []
        for m in menu.get_menu_items():        
            super().append_menu_group_keyboard(m, keyboard)        
        
        reply_markup = InlineKeyboardMarkup(keyboard, row_width = 1)
        s = 'נא לבחור'
        update.message.reply_text(text = s, reply_markup=reply_markup)

        self.__class__ = SelectMenuItemState
    
        return order, current_menu_item   

class SelectMenuItemState(OrderState):

    def callback_query_handler(self, update, context, order: Order, menu: Menu, current_menu_item: MenuGroup):
        query = update.callback_query
        query.answer()
        
        if (query.data == 'finish_order'):
            query.edit_message_text(text = "הזמנה:", reply_markup= self.create_inline_keyboard_for_order(current_menu_item, order))                    
            self.__class__ = PlaceOrderState
            return order, current_menu_item

        if (query.data.startswith("menu_group") == True):
            arr = query.data.split(':')
            current_menu_item = menu.get_menu_item(arr[1])
        else:
            operationOrderQueryHadler  = OperationOrderQueryHadler()
            operationOrderQueryHadler.handle_query(query, menu, order)

        query.edit_message_text(text = "נא לבחור", reply_markup= super().create_inline_keyboard_for_menu(current_menu_item, menu, order, current_menu_item))
        return order, current_menu_item

    def conversation_state(self):
        return SELECT_MENU_ITEM

class PlaceOrderState(OrderState):

    def callback_query_handler(self, update, context, order: Order, menu: Menu, current_menu_item: MenuGroup):
        query = update.callback_query
        query.answer()

        if (query.data == 'pay'):
            keyboard = []
            keyboard.append([InlineKeyboardButton(text=f'{self.checkIcon}סיים', callback_data = "ok"), InlineKeyboardButton(text=f'{self.crossIcon}לבטל', callback_data = "cancel")])
            query.edit_message_text(text = "הזמנה", reply_markup=InlineKeyboardMarkup(keyboard))  
            self.__class__ = PayOrderState           
            return order, current_menu_item
        
        if (query.data.startswith("menu_group") == True):
            arr = query.data.split(':')
            current_menu_item = menu.get_menu_item(arr[1])
            query.edit_message_text(text = "נא לבחור", reply_markup= super().create_inline_keyboard_for_menu(current_menu_item, menu, order, current_menu_item))        
            self.__class__ = SelectMenuItemState 
            return order, current_menu_item
        
        operationOrderQueryHadler = OperationOrderQueryHadler()

        if (operationOrderQueryHadler.can_handle_query(query)):
            operationOrderQueryHadler.handle_query(query, menu, order)
        
        if (len(order.get_order_items()) > 0):    
            query.edit_message_text(text = "הזמנה", reply_markup= super().create_inline_keyboard_for_order(current_menu_item, order))        
        else:
            query.edit_message_text(text = "נא לבחור", reply_markup= super().create_inline_keyboard_for_menu(current_menu_item, menu, order, current_menu_item))        
            self.__class__ = SelectMenuItemState 
        
        return order, current_menu_item

    def conversation_state(self):
        return PLACE_ORDER

class PayOrderState(OrderState):
    def callback_query_handler(self, update, context, order: Order, menu: Menu, current_menu_item: MenuGroup):
        query = update.callback_query
        query.answer()

        if (query.data != "ok"):
            query.edit_message_text('ההזמנה שלך בוטלה')
        else:
            query.edit_message_text('תודה! ההזמנה שלך נשלחה')
            orderSerializer = OrderSerializer()
            orderSerializer.serialize(order, 'order.txt')

        self.__class__ = FinishOrderState 

        del order
        del current_menu_item

        return None, None 

    def conversation_state(self):
        return PAY_ORDER

class FinishOrderState(OrderState):
    def callback_query_handler(self, update, context, order: Order, menu: Menu, current_menu_item: MenuGroup):
        pass
    def conversation_state(self):
        return FINISH_ORDER
