#!/usr/bin/env python3.5
import json
import helper.util as util
from helper.StateHandler import StateHandler
from game.player import Player
from game.gamedata import GameData
from helper.State import State

# define States
START, LIST, CHOOSE, SAVE, QUIT = range(5)

#States of choose
# DUNGEON = range(1)


class Start (State):
    def run(self, gamedata):
        print("Welcome to the village. You have quite a few things you could do. Or you could just do nothing. Doing nothing is good. Just do nothing. Always keep in mind. Everything you do will cause the death of a sweet little penguin... maybe.")
        return LIST, gamedata
    def next(self, next_state):
        if(next_state == LIST):
            return States['List']

class List (State):
    def run(self, gamedata):
        print("Your destinations are:")
        print("0\tDungeon")
        print("1\tInventory")
        print("2\tRetailer")
        print("3\tSmith")
        print("4\tDruid")
        print("5\tSave")
        print("6\tQuit")

        return CHOOSE, gamedata
        
    def next(self, next_state):
        if(next_state == CHOOSE):
            return States['Choose']

class Choose (State):
    def run(self, gamedata):
        try:
            value = int(input("> "))
            if value == 0:
            elif value == 1:
                pass
            elif value >= 2 and value <=4:
                pass
            elif value == 5:
                return SAVE, gamedata
            elif value == 6:
                return QUIT, gamedata
            else:
                return LIST, gamedata
            
        except ValueError as err:
            return LIST, gamedata
        
    def next(self, next_state):
        if next_state == SAVE:
            return States['Save']
        elif next_state == QUIT:
            return States['Quit']
        elif next_state == LIST:
            return States['List']

class Save(State):
    def run (self, gamedata):
        try:
            with open("player.json", "w") as outfile:
                json.dump(gamedata.player, outfile, cls=util.CustomEncoder)
            return LIST, gamedata
        except IOError:
            print("Could not save game data!")
        else:
            return None, gamedata
             
    def next(self, next_state):
        if(next_state == LIST):
            return States['List']
        else:
            pass

class Quit (State):
    def run(self, gamedata):
        print("Do you want to save the game before exiting? (Y/N)")
        value = input()
        if value.lower() == "y":
            return SAVE, gamedata
        else:
            return None, gamedata
    def next(self, next_state):
        pass

class End (State):
    def run(self, gamedata):
        return None, gamedata
    def next(self, next_state):
        pass

States = {
    'Start': Start(),
    'List': List(),
    'Choose': Choose(),
    'Save': Save(),
    'Quit': Quit()
}


class Handler(StateHandler):
    def __init__(self, gamedata):
        statesList = list(States.values())
        StateHandler.__init__(self, States["Start"], statesList,
                              End(), gamedata)

class Village():
    def run(self, gamedata):
        try:
            Handler(gamedata).run()
            return True, gamedata
        except:
            return False, gamedata

if __name__ == '__main__':
    gamedata = GameData()
    Handler(gamedata).run()
