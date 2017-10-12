#!/usr/bin/env python3.5

import json
from game.player import Player
from game.item import Item
from game.inventory import Inventory
from game.inventory import InventoryItem
from game.attributes import Attributes
from game.gear import Gear


def is_this_correct():
  print("Is this correct? (Y/N)")
  value = input()
  if value.lower() == "y":
    return True
  elif value.lower() == "n":
    return False
  else:
    raise ValueError("invalid")

def validate_input(objectType, recursive, length, startString="> "):
  try:
    valueString = input(startString)
    if length and len(valueString) > length :
      if recursive: 
        return validate_input(objectType, recursive, length, startString)
      else:
        return False, None 
    else:
      value = objectType(valueString)
      return True, value
      
  except (ValueError, TypeError): 
    if recursive: 
      return validate_input(objectType, recursive, length, startString)
    else:
      return False, None  

def validate_item_input(items):
  success, string = validate_input(str, False, None)
  if string == 'quit':
    return False, string
  activeItem = None
  if success:
    for item in items:
      if item.name == string:
        activeItem = item
        break
    if activeItem:
      return True, activeItem
  return False, None


def print_character(character):
  print("Name: {0}".format(character.name))
  print("\tStrength: {0}".format(character.attributes.strength))
  print("\tAgility: {0}".format(character.attributes.agility))
  print("\tSpeed: {0}".format(character.attributes.speed))
  print("\tDefense: {0}".format(character.attributes.defense))

def load_data(savefile="data.json"):
  fp = open(savefile, "r")
  items = json.load(fp)
  fp.close()
  return items

def load_village(savefile="data.json"):
  village = load_data(savefile)['village']
  return village

def load_items(savefile="data.json"):
  data = load_data(savefile)
  items = []
  for item in data['items']:
    items.append(Item(**item))
  return items

def load_player(savefile="player.json"):
  fp = open(savefile, "r")
  player = Player(**json.load(fp))
  fp.close()
  inventory = Inventory()
  for inventoryItem in player.inventory['items']:
    inventory.add(Item(**inventoryItem['item']), inventoryItem['amount']) 
  player.inventory = inventory
   
  gearTypes = {}
  for key, value in player.gear.items():
    gearTypes[key] = Item(**value) if value else None 

  player.gear = Gear(**gearTypes)

  return player


class CustomEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Player):
      return obj.__dict__
    if isinstance(obj, Item):
      return obj.__dict__
    if isinstance(obj, Inventory):
      return obj.__dict__
    if isinstance(obj, InventoryItem):
      return obj.__dict__  
    if isinstance(obj, Gear):
      return obj.__dict__  
    else:
      return json.JSONEncoder.default(self,obj)


  

if __name__ == '__main__':
  pass
  # print(load_player('p_items.new.json').inventory.items[0].item.name)
  # player = load_player('player.json')
  # print(player.inventory.items[0].item.item.name)
  # print(load_items()[5].name)

