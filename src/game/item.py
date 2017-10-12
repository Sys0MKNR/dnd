#!/usr/bin/env python3.5

class Item:
  def __init__(self, **item):
    self.name = ""
    self.price = 0
    self.influenced_attribute = ""
    self.value = 0
    self.type = ""
    self.gearType = ""
    self.__dict__.update(item)



