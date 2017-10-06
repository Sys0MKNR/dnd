#!/usr/bin/env python3.5

import json
from game.player import Player
from game.item import Item


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
  print("Class: {0}".format(character.type))
  print("Attributes:")
  print("\tStrength: {0}".format(character.strength))
  print("\tAgility: {0}".format(character.agility))
  print("\tSpeed: {0}".format(character.speed))
  print("\tDefense: {0}".format(character.defense))
  print("\tSpecial Skill: {0}".format(character.special))

def load_player(savefile):
  fp = open(savefile, "r")
  player = Player(**json.load(fp))
  fp.close()
  items = []
  for dict_item in player.inventory:
    item = Item(**dict_item)
    items.append(item)
  player.inventory = items
  return player


class CustomEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Player):
      return obj.__dict__
    if isinstance(obj, Item):
      return obj.__dict__
    else:
      return json.JSONEncoder.default(self,obj)

