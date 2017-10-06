#!/usr/bin/env python3.5

import helper.util
from helper.StateHandler import StateHandler
from game.player import Player
from game.gamedata import GameData
from helper.State import State
from states import getStates


class Quit(State):
    def run(self, gamedata):
        return None, gamedata

    def next(self, x):
        pass


class Handler(StateHandler):
    def __init__(self, gamedata):
        states = getStates()
        statesList = list(states.values())
        StateHandler.__init__(self, states["Start"], statesList,
                              Quit(), gamedata)

class CreateChar(State):
    def run(self, gamedata):
        return None, gamedata

    def next(self, x):
        pass

if __name__ == '__main__':
    gamedata = GameData()
    Handler(gamedata).run()
