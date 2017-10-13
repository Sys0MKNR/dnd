#!/usr/bin/env python3.5
import json
import sys
import helper.util as util
from helper.StateHandler import StateHandler
from game.player import Player
from game.gamedata import GameData
from helper.State import State
from states.villager import Villager
from states.dungeon import Dungeon


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

        if gamedata.bonus:
            print("7\tChest") 
            print("8\tGrave Digger")

        return CHOOSE, gamedata
        
    def next(self, next_state):
        if(next_state == CHOOSE):
            return States['Choose']

def handleChest(gamedata):
    print("Welcome to your chest.")
    while True:
        print("Type 'quit' or 'store'/'take' to either leave or choose a inventory mode.")
        value = input("> ")
        if value == "quit":
            break
        elif value == 'take':
            while True:
                print("You have these items in your chest:")
                for item in gamedata.player.villageChest.items:
                    print("x{0}\t{1}".format(item.amount, item.name))
                print("Type 'quit' or the name of the item you want to pickup")
                success, foundItem = util.validate_item_input(gamedata.player.villageChest.items)
                if foundItem == 'quit':
                    break
                
                elif success:
                    gamedata.player.villageChest.remove(foundItem) 
                    gamedata.player.add_item(foundItem.item)
                    print("Put {0} into your inventory".format(foundItem.name))                

        elif value == 'store':
            while True:
                print("You have these items in your inventory:")
                for item in gamedata.player.inventory.items:
                    print("x{0}\t{1}".format(item.amount, item.name))
                print("Type 'quit' or the name of the item you want to store")
                success, foundItem = util.validate_item_input(gamedata.player.inventory.items)
                if foundItem == 'quit':
                    break
                
                elif success:   
                    print(foundItem.name)
                    gamedata.player.villageChest.add(foundItem)  
                    gamedata.player.drop_item(foundItem)   
       
        else: 
            continue
    return gamedata

def handleGraveDigger(gamedata):
    print("Welcome to the grave digger. If you died recently then I should be able to help you")
    while True:
        print("You have {0} gold.".format(gamedata.player.gold))
        print("I can sell you these items:")
        for item in gamedata.graveDigger.items:
            print("x{0}\t{1} for {2} gold".format(item.amount, item.name, item.item.price))
        print("Type 'quit' or the name of the item you want to buy.")
        success, foundItem = util.validate_item_input(gamedata.graveDigger.items)
        if foundItem == 'quit':
            break
                
        elif success:
            gamedata.graveDigger.remove(foundItem) 
            if gamedata.player.buy_item(foundItem.item, 0.5):
                print("Put {0} into your inventory".format(foundItem.name))  
            else: 
                print("Not enough gold. You have {0} gold left.".format(gamedata.player.gold)) 

    return gamedata   

class Choose (State):
    def run(self, gamedata):
        success, value = util.validate_input(str, False, 1)
        if success:
            if gamedata.bonus:
                success = False
                if value == '7':
                    gamedata = handleChest(gamedata)
                    success = True

                elif value == '8':
                    gamedata = handleGraveDigger(gamedata)
                    success = True
                    
                if success: 
                    return START, gamedata

            opt = gamedata.village['opts'][value]
            try:
                if opt['obj']:
                    getattr(gamedata.player, opt['action'])()

            except KeyError as err:
                
                if opt['class']:                    
                    c = getattr(sys.modules[__name__], opt['class'])
                    success, gamedata = c().run(*parseParams(opt['params'], gamedata))    
                    
                else: 
                    return getattr(sys.modules[__name__], opt['callback']), gamedata               
                
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
            return False, gamedata


