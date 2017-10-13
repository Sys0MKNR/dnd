#!/usr/bin/env python3.5

import helper.util as util

class GameData:
  def __init__(self, **gamedata):
    self.player = None
    self.items = util.load_items()
    self.village = util.load_village()
    self.activeVillager = None
    self.quitting = False
    self.dungeon = None
    self.bonus = False