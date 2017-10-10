#!/usr/bin/env python3.5
import helper.util as util
from helper.StateHandler import StateHandler
from game.player import Player
from game.gamedata import GameData
from helper.State import State
from game.item import Item
from game.inventory import Inventory
from states.createChar import CreateChar

# define States
START, LIST, CHOOSE = range(3)


class Retailer():
    def __init__(self, gamedata):
        print("Welcome to the Retailer {0}!".format(gamedata.player.name))
        while True:
            inventory = gamedata.player.inventory
            if inventory.items:
                print("This is what I would pay for your Items:")
                for item in inventory.items:
                    print("* {0} for {1} gold".format(item.name, int(item.price*0.5)))
                print("You have {0} gold.".format(gamedata.player.gold)) 
                print("Type 'quit' or the name of the item you want to sell:")

                itemName = input("> ")

                if itemName == 'quit':
                    break
                elif inventory.isItemInInventory(itemName):
                    gold = gamedata.player.inventory.sell(itemName)
                    gamedata.player.gold += gold
                    print("You have choosen {0}.\n You now have {1} gold.\n Removed item from Inventory.".format(itemName, gamedata.player.gold ))
                else: 
                    print("You dont own this item.")
                    continue
                            
            else: 
                print("Sorry, you have nothing to sell,\n Thanks for visiting!")
                break
#gear and potions
class SellNPC():
    def __init__(self, gamedata, sells):
        print("Welcome to the store {0}!\n You have {1} gold to spend for {2}. This is what I'm selling:".format(gamedata.player.name, gamedata.player.gold, sells))
        
        items = [x for x in gamedata.items if x.type == sells]
        
        while True:          
            for item in items:
                print("* {0} for {1} gold +{2} {3}".format(item.name, item.price, item.value, item.influenced_attribute))
            print("You have {0} gold.".format(gamedata.player.gold)) 
            print("Type 'quit' or the name of the item you want to buy:")

            itemName = input("> ")

            if itemName == 'quit':
                break
            else:
                for item in items:
                    print(item)
                    if item.name == itemName:
                        gold = gamedata.player.inventory.buy(item)
                        if (gamedata.player.gold - gold) >= 0:
                            gamedata.player.gold -= gold
                            print("You have choosen {0}.\n You  have {1} gold left.".format(itemName, gamedata.player.gold ))
                        else: 
                            print("You dont have enough gold for this item!")
                        break
                    else:                                      
                        print("I dont sell this item.")
        print("Thanks for visiting!")             



class Start(State):
    def run(self, gamedata):
        return LIST, gamedata

    def next(self, next_state):
        if next_state == LIST:
            return States['List']

class List(State):
    def run(self, gamedata):
        print("Choose a Villager.")
        print("1 Retailer")
        print("2 Druid")
        print("3 Smith")
        return CHOOSE, gamedata

    def next(self, next_state):
        if next_state == CHOOSE:
            return States['Choose']

class Choose(State):
    def run(self, gamedata):
        
        try:
            value = int(input("> "))
            
            if value == 1:
                Retailer(gamedata)
            elif value == 2:
                SellNPC(gamedata, "potion")
            elif value == 3:
                SellNPC(gamedata, "gear")
            else:
                return LIST, gamedata

        except ValueError:
            return LIST, gamedata
        return None, gamedata

    def next(self, next_state):
        if next_state == LIST:
            return States['List']
        else:
            pass

class Quit (State):
    def run(self, gamedata):
        return None, gamedata
    def next(self, next_state):
        pass

States = {
    'Start': Start(),
    'List': List(),
    'Choose': Choose()
}

class Handler(StateHandler):
    def __init__(self, gamedata):
        statesList = list(States.values())
        StateHandler.__init__(self, States["Start"], statesList,
                              Quit(), gamedata)

class Villager():
    def run(self, gamedata):
        try:
            Handler(gamedata).run()
            return True, gamedata
        except:
            return False, gamedata

if __name__ == '__main__':
    gamedata = GameData()
    gamedata.player = util.load_player('p_items.json')
    success, gamedata = Villager().run(gamedata)
    # SellNPC(gamedata, "gear")
    # Retailer(gamedata)