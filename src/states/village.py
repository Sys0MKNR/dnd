#!/usr/bin/env python3.5
import json
import sys
import helper.util as util
from helper.StateHandler import StateHandler
from game.player import Player
from game.gamedata import GameData
from helper.State import State
from states.villager import Villager


# define States
START, LIST, CHOOSE, SAVE, QUIT = range(5)


def parseParams(params, gamedata):
    for i, param in enumerate(params):
        if param == 'standard':
            params[i] = gamedata
    
    return params


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

        for key, opt in sorted(gamedata.village['opts'].items()):
            print("{0}\t{1}".format(key, opt["name"]))        

        return CHOOSE, gamedata
        
    def next(self, next_state):
        if(next_state == CHOOSE):
            return States['Choose']

class Choose (State):
    def run(self, gamedata):
        success, value = util.validate_input(str, False, 1,)
        print(success)
        if success:
            opt = gamedata.village['opts'][value]
            try:
                if opt['obj']:
                    getattr(gamedata.player, opt['action'])()

            except KeyError as err:

                if(opt['class']):                    
                    c = getattr(sys.modules[__name__], opt['class'])
                    success, gamedata = c().run(*parseParams(opt['params'], gamedata))    
        
                else: 
                    return getattr(sys.modules[__name__], opt['callback']), gamedata               
                
            print(gamedata.player.gold)
            return START, gamedata    
        else:
            return START, gamedata            
            
        
    def next(self, next_state):
        if next_state == SAVE:
            return States['Save']
        elif next_state == QUIT:
            return States['Quit']
        elif next_state == START:
            return States['Start']

class Save(State):
    def run (self, gamedata):
        try:
            with open("player.json", "w") as outfile:
                json.dump(gamedata.player, outfile, cls=util.CustomEncoder)
            
        except IOError:
            print("Could not save game data!")

        if gamedata.quitting:
            return None, gamedata
        else:
            return LIST, gamedata
             
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
            gamedata.quitting = True
            return SAVE, gamedata
        else:
            return None, gamedata
    def next(self, next_state):
        if next_state == SAVE:
            return States['Save']
        else: 
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
            gamedata = Handler(gamedata).run()
            return True, gamedata
        except Exception as err:
            print(err)
            return False, gamedata


if __name__ == '__main__':
    gamedata = GameData()
    gamedata.player = util.load_player()
    Handler(gamedata).run()
