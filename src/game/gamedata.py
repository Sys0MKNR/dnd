#!/usr/bin/env python3.5

import helper.util as util
from game.inventory import Inventory

class GameData:
  def __init__(self, **gamedata):
    self.player = None
    self.items = util.load_items()
    self.village = util.load_village()
    self.activeVillager = None
    self.quitting = False
    self.dungeon = None
    self.bonus = False
    self.graveDigger = Inventory()