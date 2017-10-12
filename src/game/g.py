#!/usr/bin/env python3.5

import helper.util as util
from states.createChar import CreateChar
from game.gamedata import GameData


class Game():
    def __init__(self, args):
        print(args)
        gamedata = GameData()
        if args.create_player:
            succes, gamedata = CreateChar().run(gamedata)
        elif args.savefile:
            try:
                gamedata.player = util.load_player(args.savefile)
            except IOError:
                print("Error while loading the player. This probably happens because of a wrong filepath.")
                return
        else:
            print("usage: python3.5 main.py [--savefile SAVEFILE] [--create-player]")
            return

        Village.

        
