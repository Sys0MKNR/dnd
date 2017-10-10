#!/usr/bin/env python3.5

from game.attributes import Attributes
from game.inventory import Inventory

class Player:
  def __init__(self, **player):
    self.name = ""
    self.lvl = 1
    self.xp =  0
    self.gold = 100 
    self.hp = 100
    self.attributes = Attributes()
    self.inventory = Inventory()
    self.__dict__.update(player)
