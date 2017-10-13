
import random
import helper.util as util
from helper.StateHandler import StateHandler
from helper.State import State
from game.gamedata import GameData
from game.inventory import Inventory
from game.gear import Gear

START, LOOK, MOVE, OPEN,  ATTACK, FIGHT, INVENTORY, MENU, SUCCESS, EXIT = range(10)

DUNGEON = util.load_data()['dungeon']
DUNGEON_ENEMIES = DUNGEON['enemies']
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
        
        success, value = util.validate_input(int, False, 1)

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
                return MENU, gamedata
            else:                
                return FIGHT, gamedata

        else: 
            print("There is no enemy.")
            return MENU, gamedata
        
    def next(self, next_state):
        if next_state == MENU:
            return States['Menu']
        elif next_state == FIGHT:
            return States['Fight']

def lower_defense(defense, hits):
    if hits > 3: 
        return 0
    elif hits > 0:
        defense = int(float(defense) * (1- (float(hits) * 0.25))) 
        print(defense)
    return defense

def attack(attacker, defender):

    totalAgility = attacker.agility + defender.agility
    try:
        agilityPercentage = attacker.agility / totalAgility
        if random.random() < agilityPercentage:
            return False, 0
        else:
            damageToEnemy = gamedata.player.strength - lower_defense(defender.defense, defender.hits)  
            if damageToEnemy > 0:
                return True, damageToEnemy
    except ZeroDivisionError:
        damageToEnemy = gamedata.player.strength - lower_defense(defender.defense, defender.hits)  
        if damageToEnemy > 0:
            return True, damageToEnemy
    return True, 0


class Fight(State):
    def run(self, gamedata):
        dead = False
        for index, enemy in enumerate(gamedata.dungeon.activeRoom.enemies):
            if enemy.speed > gamedata.player.speed:
                hit, damage = attack(enemy, gamedata.player)
                if hit:
                    gamedata.player.hits += 1
                    gamedata.player.hp -= damage
                    print("{0} hit you and dealt {1} damage.".format(enemy.type, damage))

        while True:
            enemiesDead = True
            for index, enemy in sorted(enumerate(gamedata.dungeon.activeRoom.enemies)):
                if enemy.hp > 0:
                    enemiesDead = False
                    print("{0} {1}".format(index, enemy))
            if enemiesDead: 
                gamedata.player.hits = 0
                print("You killed all enemies in this room.")
                gamedata.dungeon.activeRoom.clear = True
                return MENU, gamedata
            print('Which enemy would you like to attack?')
            print('Your hp: {0}'.format(gamedata.player.hp))
            success, value = util.validate_input(int, 1, None)
            if success:
                enemy = gamedata.dungeon.activeRoom.enemies[value]
                if enemy.hp <= 0:
                    continue
                hit, damage = attack(gamedata.player, enemy)
                if hit:
                    gamedata.dungeon.activeRoom.enemies[value].hits += 1
                    gamedata.dungeon.activeRoom.enemies[value].hp -= damage
                    print("You attacked {0} and dealt {1} damage.".format(enemy.type, damage))
                    if gamedata.dungeon.activeRoom.enemies[value].hp <= 0:
                        gold = gamedata.dungeon.activeRoom.enemies[value].lvl * 10 + 1
                        xp = gamedata.dungeon.activeRoom.enemies[value].lvl * 100 + 10
                        gamedata.player.gold += gold
                        gamedata.player.xp += xp
                        print("You killed {0} and got {1} gold and {2} xp.".format(enemy.type, gold, xp))
                    else: 
                        hit, damage = attack(enemy, gamedata.player)
                        if hit:
                            gamedata.player.hits += 1
                            gamedata.player.hp -= damage
                            print("{0} hit you and dealt {1} damage.".format(enemy.type, damage))
                            if gamedata.player.hp <= 0: 
                                dead = True
                                break
        if dead: 
            gamedata.dungeon = None
            gamedata.player.inventory = Inventory()
            gamedata.player.gear = Gear()
            gamedata.player.hp = 100
            gamedata.player.hits = 0
            print("You died. You will return to the village.")
            return EXIT, gamedata
        else:
            if gamedata.activeRoom.enemies[0].type == 'boss':
                print('success')
                return SUCCESS, gamedata
            else:
                return MENU, gamedata


    def next(self, next_state):
        if next_state == MENU:
            return States['Menu']
        elif next_state == EXIT:
            return States['Exit']   

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
        loot = random.choice(ITEMS)
        print("The boss dropped {0}.".format(loot.name))
        gamedata.player.add_item(loot)
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


def generateDungeon(gamedata):
    rooms = []
    rooms.append(Room(gamedata))

    chest = False
    for x in range(3):
        if random.choice((True, False)) and not chest:
            rooms.append(Room(gamedata,'chest'))
            chest = True
        else:
            rooms.append(Room(gamedata, 'enemy'))

    rooms.append(Room(gamedata, 'boss'))

    return rooms


class Room():
    def __init__(self,gamedata, _type="start"):
        self.type = _type
        self.enemies = None
        self.chest = None
        self.clear = False

        if _type == 'enemy':
            self.enemies = []
            for x in range(3):
                if random.choice((True, False)):
                    self.enemies.append(generateEnemy(gamedata.player))
            if not self.enemies:
                self.enemies.append(generateEnemy(gamedata.player))
            
        elif _type == 'chest':
            self.chest = Chest()
        elif _type == 'boss':
            self.enemies = []
            self.enemies.append(generateEnemy(gamedata.player, True))
        elif _type == 'start':
            self.clear = True
    
class Chest():
    def __init__(self):
        self.item = random.choice(ITEMS)


def generateEnemy(player, boss=False):
    _type = random.choice(list(DUNGEON_ENEMIES))
    enemy = DUNGEON_ENEMIES[_type]

    opts = {
        "lvl": 0,
        'hp': 0,
        'xp': 0,
        'strength': 0,
        'agility': 0,
        'speed': 0,
        'defense': 0,
    }

    for key in list(opts):
        playerValue = getattr(player, key)
        percentage = 0
        if boss:
            percentage = random.randint(90, 110)/100
        else:
            percentage = random.randint(enemy['from'], enemy['to'])/100
        opts[key] = int(float(playerValue) * percentage)

    opts['type'] = _type

    return Enemy(**opts)


class Enemy():
    def __init__(self, **enemy):
        self.type = ""
        self.lvl = 0
        self.hp = 0
        self.xp = 0
        self.strength = 0
        self.agility = 0
        self.speed = 0
        self.defense = 0
        self.hits = 0
        self.__dict__.update(enemy)

    def __str__(self):
        return "{0} ({1} HP)".format(self.type, self.hp)


class Dungeon():
    def run(self, gamedata):

        try:
            self.text = random.choice(DUNGEON['texts'])
            self.rooms = generateDungeon(gamedata)
            self.index = 0
            self.activeRoom = self.rooms[self.index]
            print(self.text)
            gamedata.dungeon = self
            gamedata = Handler(gamedata).run()
            return True, gamedata
        except Exception as e:
            print(e)
            return False, gamedata





if __name__ == '__main__':
    gamedata = GameData()
    gamedata.player = util.load_player('player.json')
    Dungeon().run(gamedata)
