#!/usr/bin/env python3.5

from game.inventory import Inventory
from game.gear import Gear



class Player:
    def __init__(self, **player):
        self.name = ""
        self.type = ""
        self.strength = 0
        self.agility = 0
        self.speed = 0
        self.defense = 0
        self.special = 0
        self.lvl = 1
        self.xp = 0
        self.gold = 100
        self.hp = 100
        self.inventory = Inventory()
        self.gear = Gear()
        self.hits = 0
        self.villageChest = Inventory()
        self.__dict__.update(player)

    #item is InventoryItem
    def sell_item(self, item, sellPrice):
        self.inventory.remove(item)
        self.gold += sellPrice
        return True

    #item is Item
    def buy_item(self, item, multiplier=1):
        if self.gold - (item.price * multiplier) < 0:
            return False
        else:
            self.inventory.add(item)
            self.gold -= (item.price * multiplier)
            return True

    def use_item(self, item):
        if item.item.type == "potion":
            oldValue = getattr(self, item.item.influenced_attribute)
            setattr(self, item.item.influenced_attribute, oldValue + item.item.value)
        elif item.item.type == "gear":
            self.replace_gear(item)
        elif item.item.type == "special":
            if item.item.name == "Portal":
                pass
        self.drop_item(item)

    def drop_item(self, item):
        self.inventory.remove(item)
        return True
    
    def add_item(self, item):
        self.inventory.add(item)
    
    def replace_gear(self, item):
        print(self.gear)
        oldGear = getattr(self.gear, item.item.gearType)
        inf_attr = item.item.influenced_attribute
        if oldGear:
              
            if inf_attr == oldGear.influenced_attribute:
                oldValue = getattr(self, inf_attr)
                oldGearValue = oldGear.value
                newValue = item.item.value  
                setattr(self, inf_attr, oldValue - oldGearValue + newValue)
            
            else: 
                oldValue = getattr(self, oldGear.influenced_attribute)
                oldGearValue = oldGear.value
                setattr(self, oldGear.influenced_attribute, oldValue - oldGearValue)
                
                otherOldvalue = getattr(self, inf_attr)
                newValue = item.item.value    
                setattr(self, inf_attr, otherOldvalue + newValue)

            self.inventory.add(oldGear)

        else:            
            oldValue = getattr(self, inf_attr)  
            newValue = item.item.value    
            setattr(self, inf_attr, oldValue + newValue)
            
        setattr(self.gear, item.item.gearType, item.item)

    def open_inventory(self):
        print("Welcome to your inventory {0}".format(self.name))
        while True:
            print("These are your items:")
            for inventoryItem in self.inventory.items:
                item = inventoryItem.item

                print("x{0} {1} \t--increases {2} by {3}".format(inventoryItem.amount, item.name,
                                                                item.influenced_attribute, item.value))
            print("Type 'quit' or the name of the item you want to use/drop")
            value = input("> ")

            if value == "quit":
                break

            choosenItem = [
                item for item in self.inventory.items if item.name == value]

            if not choosenItem:
                continue

            choosenItem = choosenItem[0]

            print("Do you want to 'use' or 'drop' the {0}? Else 'quit' ".format(choosenItem.name))

            value = input("> ")

            if value == 'quit':
                break
            elif value == 'use':
                self.use_item(choosenItem)
                print("The item was used.")
            elif value == 'drop':
                self.drop_item(choosenItem)
                print("The item was dropped.")
            else:
                continue
