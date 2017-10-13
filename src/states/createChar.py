#!/usr/bin/env python3.5
import json
import helper.util as util
from helper.StateHandler import StateHandler
from game.player import Player
from game.gamedata import GameData
from helper.State import State

# define States
START, STRENGTH, AGILITY, SPEED, DEFENSE, CONFIRM, STORE = range(7)

def askForStat(stat):
    while True:
        try:
            value = int(input(stat+"> "))
            return value
        except ValueError as err:
            pass

def checkStatPoints(player):
    if (player.strength + player.agility + player.speed + player.defense) <= 100:
        return True
    else:
        return False

class Start(State):
    def run(self, gamedata):
        print("Welcome to P0 Dungeon Quest character creator")
        print("Give us a name to call you:")
        
        while True:
            name = input("> ")
            if name:
                break
        
        print("{0} is the name you want to choose?".format(name))
        while True:
            try:
                correct = util.is_this_correct()
                if correct:
                    gamedata.player = Player()
                    gamedata.player.name = name
                    return STRENGTH, gamedata
                else:
                    return START, gamedata
                    
            except ValueError as err:
                print("Please enter Y/y for yes or N/n for no!")

    def next(self, next_state):
        if next_state == START:
            return States['Start']
        elif next_state == STRENGTH:
            return States['Strength']

class Strength (State):
    def run(self, gamedata):
        print("You have 100 points to assign to your character.\nStart now to assign those Points to your characters strength, agility, speed and defense.")
        gamedata.player.strength = askForStat("Strength")
        return AGILITY, gamedata
      
    def next(self, next_state):
        return States['Agility']

class Agility (State):
    def run(self, gamedata):
        gamedata.player.agility = askForStat("Agility")
        return SPEED, gamedata
      
    def next(self, next_state):
        return States['Speed']

class Speed (State):
    def run(self, gamedata):
        gamedata.player.speed = askForStat("Speed")
        return DEFENSE, gamedata
      
    def next(self, next_state):
        return States['Defense']

class Defense (State):
    def run(self, gamedata):
        gamedata.player.defense = askForStat("Defense")
        if(checkStatPoints(gamedata.player)):
            return CONFIRM, gamedata
        else:
            print("Sorry it seems like you spent more than 100 abillity points on your character... try that again!")
            return STRENGTH, gamedata
      
    def next(self, next_state):
        if next_state == CONFIRM:
            return States['Confirm']
        elif next_state == STRENGTH:
            return States['Strength']

class Confirm (State):
    def run(self, gamedata):
        print("Before you store your character please confirm your stats!")
        util.print_character(gamedata.player)
        while True:
            try:
                correct = util.is_this_correct()
                if correct:
                    return STORE, gamedata
                else:
                    return START, gamedata
                    
            except ValueError as err:
                print("Please enter Y/y for yes or N/n for no!")

    def next(self, next_state):
        if next_state == START:
            return States['Start']
        elif next_state == STORE:
            return States['Store']

class Store(State):
  def run (self, gamedata):
    with open("player.json", "w") as outfile:
      json.dump(gamedata.player, outfile, cls=util.CustomEncoder)
    return None, gamedata

  def next(self, next_state):
    pass



States = {
    'Start': Start(),
    'Strength': Strength(),
    'Agility': Agility(),
    'Speed': Speed(),
    'Defense': Defense(),
    'Confirm': Confirm(),
    'Store': Store()
}

class Quit(State):
    def run(self, gamedata):
        return None, gamedata

    def next(self, x):
        pass


class Handler(StateHandler):
    def __init__(self, gamedata):
        statesList = list(States.values())
        StateHandler.__init__(self, States["Start"], statesList,
                              Quit(), gamedata)

class CreateChar():
    def run(self, gamedata):
        try:
            Handler(gamedata).run()
            return True, gamedata
        except:
            return False, gamedata
        

