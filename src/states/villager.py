#!/usr/bin/env python3.5
import helper.util as util
from helper.StateHandler import StateHandler
from game.player import Player
from game.gamedata import GameData
from helper.State import State

# define States
START, LIST, CHOOSE = range(3)


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
    Handler(gamedata).run()
