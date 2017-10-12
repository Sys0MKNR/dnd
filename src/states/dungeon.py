
import random
import helper.util as util
from helper.StateHandler import StateHandler
from helper.State import State
from game.gamedata import GameData

START, LOOK, MOVE, OPEN,  ATTACK, FIGHT, INVENTORY, MENU, SUCCESS, EXIT = range(10)

DUNGEON_INFO = util.load_data()['dungeon']['texts']
ITEMS = util.load_items()


class Start(State):
    def run(self, gamedata):
        return MENU, gamedata
    def next(self, next_state):
        return States['Menu']


class Menu(State):
    def run(self, gamedata):

        gamedata.dungeon.activeRoom = gamedata.dungeon.rooms[gamedata.dungeon.index]
        print("What would you like to do?")
        print("0. look arround")
        print("1. move")
        print("2. open")
        print("3. attack")
        print("4. open inventory")
        print("5. run away (leave dungeon)")
        
        success, value = util.validate_input(int, False, None)

        options = {
            0: LOOK,
            1: MOVE,
            2: OPEN,
            3: ATTACK,
            4: INVENTORY, 
            5: EXIT
        }

        if success:
            return options[value], gamedata
        else: 
            return MENU, gamedata


    def next(self, next_state):

        if next_state == MENU: 
            return States['Menu']
        elif next_state == LOOK:
            return States['Look']
        elif next_state == MOVE:
            return States['Move']
        elif next_state == OPEN:
            return States['Open']
        elif next_state == ATTACK:
            return States['Attack']
        elif next_state == INVENTORY:
            return States['Inventory']
        elif next_state == EXIT:
            return States['Exit']                

class Look(State):
    def run(self, gamedata):
        print(gamedata.dungeon.text)
        return MENU, gamedata
    def next(self, next_state):
        return States['Menu']

class Move(State):
    def run(self, gamedata):
        if gamedata.dungeon.activeRoom.clear:
            if gamedata.dungeon.index == 4: 
                return SUCCESS, gamedata
            gamedata.dungeon.index+=1
            print('You have entered a new room!')
        else:
            print('You cant go to the next room. Clear this one first.')
        return MENU, gamedata
            
    def next(self, next_state):
        if(next_state == MENU):
            return States['Menu']

class Open(State):
    def run(self, gamedata):
        if gamedata.dungeon.activeRoom.type == 'chest':
            if gamedata.dungeon.activeRoom.clear:
                print("You already looted this chest.")

            else:                   
                item = gamedata.dungeon.activeRoom.chest.item
                gamedata.dungeon.activeRoom.clear = True
                gamedata.player.add_item(item)
                print("You found {0} in the chest.".format(item.name))

        else: 
            print("There is no chest.")

        return MENU, gamedata        

    def next(self, next_state):
        if next_state == MENU:
            return States['Menu']   


class Attack(State):
    def run(self, gamedata):
        if gamedata.dungeon.activeRoom.type == 'enemy' or gamedata.dungeon.activeRoom.type == 'boss':
            if gamedata.dungeon.activeRoom.clear:
                print("You already killed all enemies.")
            else:
                for enemy in gamedata.dungeon.activeRoom.enemies:
                    print()        


        else: 
            print("There is no enemy.")
            return MENU, gamedata
        
    def next(self, next_state):
        pass   

class Fight(State):
    def run(self, gamedata):
        pass
    def next(self, next_state):
        pass   

class Inventory(State):
    def run(self, gamedata):
        gamedata.player.open_inventory()
        return START, gamedata
    def next(self, next_state):
        if next_state == START:
            return States['Start']


class Success(State):
    def run(self, gamedata):
        print("You beat the dungeon.")
        return None, gamedata
    def next(self, next_state):
        pass   

class Exit(State):
    def run(self, gamedata):
        return None, gamedata
    def next(self, next_state):
        pass   





States = {
    'Start': Start(), 
    'Look': Look(),
    'Move': Move(),
    'Open': Open(),
    'Attack': Attack(),
    'Fight': Fight(),
    'Inventory': Inventory(),
    'Menu': Menu(),
    'Success': Success(),
    'Exit': Exit()
}



class Handler(StateHandler):
    def __init__(self, gamedata):
        statesList = list(States.values())
        StateHandler.__init__(self, States['Start'], statesList,
                              States['Exit'], gamedata)


def generateDungeon():
    rooms = []
    rooms.append(Room())

    chest = False
    for x in range(3):
        if random.choice((True, False)) and not chest:
            rooms.append(Room('chest'))
            chest = True
        else:
            rooms.append(Room('enemy'))

    rooms.append(Boss())

    return rooms


    

class Room():
    def __init__(self, _type="start"):
        self.type = _type
        self.enemies = None
        self.chest = None
        self.clear = False

        if _type == 'enemy':
            self.enemies = []
            for x in range(3)
                if random.choice((True, False)):
                    self.enemies.append(Enemy())
            
        elif _type == 'chest':
            self.chest = Chest()
        elif _type == 'boss':
            self.enemy = Boss()
        elif _type == 'start':
            self.clear = True
    


class Chest():
    def __init__(self):
        self.item = random.choice(ITEMS)


def generateEnemy():
    types: {
        'orc': {
            'hp'
        }
    }


class Enemy():
    def __init__(self):
        self.type = ""
        self.hp = 0
        pass
    def __str__(self):
        return "{0} ({1} HP)".format(self.type, self.hp)

class Boss(Enemy):
    def __init__(self):
        super().__init__()


class Dungeon():
    def __init__(self):
        self.text = random.choice(DUNGEON_INFO)
        self.rooms = generateDungeon()
        self.index = 0
        self.activeRoom = self.rooms[self.index]
        
    def run(self, gamedata):
        print(self.text)
        gamedata.dungeon = self
        gamedata = Handler(gamedata).run()
        # try:

        #     return True, gamedata
        # except Exception as e:
        #     print(e)
        #     return False, gamedata





if __name__ == '__main__':
    gamedata = GameData()
    gamedata.player = util.load_player('player.json')
    Dungeon().run(gamedata)