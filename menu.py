from treelib import Node, Tree
import json

class MenuGroup(object):
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
    
    def __str__(self):
        return f"{self.name}"

class MenuItem(object):
    def __init__(self, id: str, price: float, name: str):
        self.id = id
        self.price = price        
        self.name = name        

    def __str__(self):
        return f"{self.name}: {self.price} nis"

class Menu(object):
    def __init__(self):
        self.tree = Tree()
        
        self.tree.create_node("", "main_menu", data=MenuGroup("main_menu", "תפריט ראשי"))  # root node

        self.tree.create_node("קפוצ'ינו", "cappuccino", parent="main_menu", data=MenuGroup("cappuccino", "קפוצ'ינו"))
        self.tree.create_node("איטליה הקטנה", "little_italy", parent="cappuccino", data=MenuItem("little_italy", 70, "איטליה הקטנה"))
        self.tree.create_node("דבש סומטרי – מהדורה מוגבלת", "sumatran_honey", parent="cappuccino", data=MenuItem("sumatran_honey", 80, "דבש סומטרי – מהדורה מוגבלת"))
        self.tree.create_node("הלוחם מסומטרה", "sumatrian_warrior", parent="cappuccino", data=MenuItem("sumatrian_warrior", 70, "הלוחם מסומטרה"))
        self.tree.create_node("יירגשף בלוברי", "yirgacheffe_blueberry", parent="cappuccino", data=MenuItem("yirgacheffe_blueberry", 70, "יירגשף בלוברי"))

        self.tree.create_node("אספרסו", "espresso", parent="main_menu", data=MenuGroup("espresso", "אספרסו"))
        self.tree.create_node("מגע ברזילאי", "brazilian_touch", parent="espresso", data=MenuItem("brazilian_touch", 70, "מגע ברזילאי"))
        self.tree.create_node("מואמבוטסה – מהדורה מוגבלת", "mwambutsa", parent="espresso", data=MenuItem("mwambutsa", 70, "מואמבוטסה – מהדורה מוגבלת"))
        self.tree.create_node("נטול קפאין שוויצר", "swiss_water", parent="espresso", data=MenuItem("swiss_water", 75, "נטול קפאין שוויצר"))
        self.tree.create_node("סלוסי קלוסי משוגע", "crazy_sulawesi_kalosi", parent="espresso", data=MenuItem("crazy_sulawesi_kalosi", 60, "סלוסי קלוסי משוגע"))

        self.tree.create_node("מכונה אוטומטית", "machine", parent="main_menu", data=MenuGroup("machine", "מכונה אוטומטית"))
        self.tree.create_node("פפואה קקדו – מהדורה מוגבלת", "papua_kakadu", parent="machine", data=MenuItem("papua_kakadu", 80, "פפואה קקדו – מהדורה מוגבלת"))
        self.tree.create_node("שוקולד אתיופי", "ethiopia_chocolate", parent="machine", data=MenuItem("ethiopia_chocolate", 60, "שוקולד אתיופי"))
        self.tree.create_node("תערובת הבית", "negro_roastery_house_blend", parent="machine", data=MenuItem("negro_roastery_house_blend", 55, "תערובת הבית"))
        self.tree.create_node("תערובת יומית משתנה", "new_day_blend", parent="machine", data=MenuItem("new_day_blend", 50, "תערובת יומית משתנה"))
        self.tree.create_node("תערובת עתיקת יומין", "very_ancient_special_bBlend", parent="machine", data=MenuItem("very_ancient_special_bBlend", 60, "תערובת עתיקת יומין"))


        self.tree.create_node("מקינטה", "makineta", parent="main_menu", data=MenuGroup("makineta", "מקינטה"))
        self.tree.create_node("דבש סומטרי – מהדורה מוגבלת", "sumatran_honey_makineta", parent="makineta", data=MenuItem("sumatran_honey_makineta", 80, "דבש סומטרי – מהדורה מוגבלת"))
        self.tree.create_node("הלוחם מסומטרה", "sumatrian_warrior_makineta", parent="makineta", data=MenuItem("sumatrian_warrior_makineta", 70, "הלוחם מסומטרה"))
        self.tree.create_node("יירגשף בלוברי", "yirgacheffe_blueberry_makineta", parent="makineta", data=MenuItem("yirgacheffe_blueberry_makineta", 70, "יירגשף בלוברי"))
        self.tree.create_node("מגע ברזילאי", "brazilian_touch_makineta", parent="makineta", data=MenuItem("brazilian_touch_makineta", 50, "מגע ברזילאי"))
        self.tree.create_node("מואמבוטסה – מהדורה מוגבלת", "mwambutsa_makineta", parent="makineta", data=MenuItem("mwambutsa_makineta", 70, "מואמבוטסה – מהדורה מוגבלת"))

        self.tree.create_node("פילטר", "filter", parent="main_menu", data=MenuGroup("filter", "פילטר"))
        self.tree.create_node("דבש סומטרי – מהדורה מוגבלת", "sumatran_honey_filter", parent="filter", data=MenuItem("sumatran_honey_filter", 80, "דבש סומטרי – מהדורה מוגבלת"))
        self.tree.create_node("יירגשף בלוברי", "yirgacheffe_blueberry_filter", parent="filter", data=MenuItem("yirgacheffe_blueberry_filter", 70, "יירגשף בלוברי"))
        self.tree.create_node("מואמבוטסה – מהדורה מוגבלת", "mwambutsa_filter", parent="filter", data=MenuItem("mwambutsa_filter", 70, "מואמבוטסה – מהדורה מוגבלת"))
        self.tree.create_node("נטול קפאין שוויצר", "swiss_water_filter", parent="filter", data=MenuItem("swiss_water_filter", 75, "נטול קפאין שוויצר"))


        self.tree.create_node("שחור ישראלי", "turki", parent="main_menu", data=MenuGroup("turki", "שחור ישראלי"))
        self.tree.create_node("קפה שחור טחון – קולומביאנה", "black_colombiana", parent="turki", data=MenuItem("black_colombiana", 55, "קפה שחור טחון – קולומביאנה"))
        self.tree.create_node("קפה שחור טחון – קולומביאנה והל אתיופי", "black_сardamom", parent="turki", data=MenuItem("black_сardamom", 55, "קפה שחור טחון – קולומביאנה והל אתיופי"))                      
        
        self.tree.show()

    def get_menu_item(self, id_menu_item):
        menu_node = self.tree.get_node(id_menu_item)
        if menu_node == None:
            return None
        return menu_node.data

    def get_menu_items(self, menu_group_root: MenuGroup = None):
        if (menu_group_root == None):
            menu_root = self.tree.get_node('main_menu')
            menu_group_root = MenuGroup(menu_root.data.id, menu_root.data.name)
        menu_items = []

        for c in self.tree.children(menu_group_root.id):
            if (isinstance(c.data, MenuGroup)):
                menu_items.append(MenuGroup(c.data.id, c.data.name))
            else:
                menu_items.append(MenuItem(c.data.id, c.data.price, c.data.name))
        
        return menu_items
    
    def get_parent_menu_groups(self, menu_group: MenuGroup):
        parents = []    
        cur_node = self.tree.get_node(menu_group.id)
        cur_node = self.tree.get_node(cur_node.bpointer)

        while (cur_node != None):            
            parents.append(MenuGroup(cur_node.data.id, cur_node.data.name))
            cur_node = self.tree.get_node(cur_node.bpointer)
        return parents  

class MenuSerializer(object):
    def serialize(self, menu: Menu, file_name: str):
        with open(file_name, 'w') as outfile:    
            json.dump(menu, default = lambda o: o.__dict__, fp = outfile, indent= 3)

        