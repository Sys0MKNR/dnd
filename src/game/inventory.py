#!/usr/bin/env python3.5
class Inventory():
    def __init__(self, items=None):
        if items is None:
          items = []
        self.items = items

    def add(self, newItem, amount=1):
        found = False
        for i, item in enumerate(self.items):
            if item.name == newItem.name:
                found = True
                self.items[i].amount += 1            
        if not found:
            self.items.append(InventoryItem(newItem, amount))
    
    def remove(self, newItem):
        for i, item in enumerate(self.items):
            if item.name == newItem.name:
                self.items[i].amount -= 1  
                if self.items[i].amount <= 0:
                    del self.items[i]      


class InventoryItem():
    def __init__(self, item, amount):
        self.item = item
        self.amount = amount
        self.name = item.name