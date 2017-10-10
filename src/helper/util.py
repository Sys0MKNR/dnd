#!/usr/bin/env python3.5

import json
from game.player import Player
from game.item import Item
from game.inventory import Inventory
from game.attributes import Attributes


def isThisCorrect():
  print("Is this correct? (Y/N)")
  value = input()
  if value.lower() == "y":
    return True
  elif value.lower() == "n":
    return False
  else:
    raise ValueError("invalid")


def print_character(character):
  print("Name: {0}".format(character.name))
  print("Attributes:")
  print("\tStrength: {0}".format(character.attributes.strength))
  print("\tAgility: {0}".format(character.attributes.agility))
  print("\tSpeed: {0}".format(character.attributes.speed))
  print("\tDefense: {0}".format(character.attributes.defense))


def load_data(savefile="data.json"):
  fp = open(savefile, "r")
  items = json.load(fp)
  fp.close()
  return items

def load_items(savefile="data.json"):
  data = load_data(savefile)
  items = []
  for item in data['items']:
    items.append(Item(**item))

  return items

def load_player(savefile):
  fp = open(savefile, "r")
  player = Player(**json.load(fp))
  fp.close()
  inventory = Inventory()
  for item in player.inventory['items']:
    inventory.add(Item(**item))  

  player.inventory = inventory
  player.attributes = Attributes(**player.attributes)
  return player


class CustomEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Player):
      return obj.__dict__
    if isinstance(obj, Item):
      return obj.__dict__
    if isinstance(obj, Inventory):
      return obj.__dict__
    if isinstance(obj, Attributes):
      return obj.__dict__
    else:
      return json.JSONEncoder.default(self,obj)


  

if __name__ == '__main__':
  # print(load_player('p_items.json').inventory.items[0].name)
  print(load_items()[5].name)