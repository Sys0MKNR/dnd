#!/usr/bin/env python3.5

import helper.util as util
from helper.StateHandler import StateHandler
from helper.State import State
from game.gamedata import GameData
from game.inventory import InventoryItem

START, LIST, CHOOSE = range(3)

def parseParams(params, gamedata, item=None):
    arr = []
    for param in params:
        obj, attribute = param.split(".")
        if obj == 'player':
            arr.append(getattr(gamedata.player, attribute))
        elif obj == 'item':
            if isinstance(item, InventoryItem):
                item = item.item
            arr.append(getattr(item, attribute))
    return arr


class VillagerActions:
    @staticmethod
    def buy(gamedata, item):
        item = item.item
        return gamedata.player.sell_item(item, int(item.price*0.5))
    @staticmethod
    def sell(gamedata, item):
       return gamedata.player.buy_item(item)
       

class Start(State):
    def run(self, gamedata):
        welcome = gamedata.activeVillager['welcome']
        print(welcome['text'].format(*parseParams(welcome['params'], gamedata)))      
        return LIST, gamedata

    def next(self, next_state):
        if next_state == LIST:
            return States['List']

class List(State):
    def run(self, gamedata):
        
        villager = gamedata.activeVillager
        print(villager['listmsg'])
        items = []

        if villager['action'] == "buy":
            items = gamedata.player.inventory.items
  
        elif villager['action'] == "sell":
            items = items if villager['items'] == 'all' else [item for item in gamedata.items if item.type == villager['items']]

        gamedata.activeVillager['itemObjs'] = items

        for item in items:
            print(villager['list']['text'].format(*parseParams(villager['list']['params'], gamedata, item)))

        return CHOOSE, gamedata

    def next(self, next_state):
        if next_state == CHOOSE:
            return States['Choose']

class Choose(State):
    def run(self, gamedata):
        villager = gamedata.activeVillager
        print(villager['choose'])
        success, item = util.validate_item_input(villager['itemObjs'])

        if success:
            success = getattr(VillagerActions, villager['action'])(gamedata, item) 
            if success: 
                print(villager['success']['text'].format(*parseParams(villager['success']['params'], gamedata, item)))
            else:
                print(villager['error']['text'].format(*parseParams(villager['error']['params'], gamedata, item)))
            
            return LIST, gamedata
        elif not success and item == 'quit':
            return None, gamedata
        else:
            return LIST, gamedata
    
    def next(self, next_state):
        if next_state == LIST:
            return States['List']
        else:
            pass

class Quit (State):
    def run(self, gamedata):
        gamedata.activeVillager = None
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
        StateHandler.__init__(self, States['Start'], statesList,
                              Quit(), gamedata)


def set_active_villager(gamedata, name):
    gamedata.activeVillager = [v for v in gamedata.village['villager'] if v['name'] == name][0]
    return gamedata

class Villager():
    def run(self, gamedata, name):
        try:
            gamedata = set_active_villager(gamedata, name)
            gamedata = Handler(gamedata).run()
            print(gamedata.player.gold)
            return True, gamedata
        except Exception as e:
            print(e)
            return False, gamedata


if __name__ == '__main__':
    gamedata = GameData()
    gamedata.player = util.load_player('player.json')
    gamedata.activeVillager = gamedata.village['villager'][1]
    gamedata = Handler(gamedata).run()
    print(gamedata.player.gold)
    # print(gamedata.activeVillager)
    # List().run(gamedata)