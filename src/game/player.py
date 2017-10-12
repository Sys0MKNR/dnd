#!/usr/bin/env python3.5

from game.attributes import Attributes
from game.inventory import Inventory

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
    self.xp =  0
    self.gold = 100
    self.hp = 100
    self.inventory = Inventory()
    # self.gear = Gear()
    self.__dict__.update(player)

  #item is InventoryItem
  def sell_item(self, item, sellPrice):
      self.inventory.remove(item)
      self.gold += sellPrice
      return True

  #item is Item
  def buy_item(self, item):
    if self.gold - item.price < 0:
      return False
    else:
      self.inventory.add(item)
      self.gold -= item.price
      return True

  def use_item(self, item):
    pass

  def open_inventory(self):
    

