#!/usr/bin/env python3.5
class Inventory():
    def __init__(self, items=[]):
        self.items = items

    def sell(self, item):
        if isinstance(item, str):
            for x in self.items:
                if x.name == item:
                    item = x
        
        self.items.remove(item)
        return int(item.price*0.5)
    
    def buy(self, item):   
        self.items.append(item)
        return item.price

    def add(self, item):
        self.items.append(item)

    def use(self, item):
        self.items.remove(item) 
        return item.value
    
    def drop(self, item):
        self.items.remove(item) 

    def isItemInInventory(self, itemName):
        for item in self.items:
            if item.name == itemName:
                return True
        return False
        
