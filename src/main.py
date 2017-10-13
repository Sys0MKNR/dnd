#!/usr/bin/env python3.5

import argparse
import helper.util as util
import json
from game.g import Game

from game.player import Player
from game.gamedata import GameData

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="P0 Dungeon")
  parser.add_argument('--savefile', help="A player savefile")
  parser.add_argument("--create-player", dest="create_player", action='store_true', help="Create a player save file. Stored to player.json by default")
  parser.add_argument('-b', '--bonus', dest="bonus", action="store_true")
  parser.set_defaults(create_player=False)
  parser.set_defaults(bonus=False)
  args = parser.parse_args()

  Game(args)
