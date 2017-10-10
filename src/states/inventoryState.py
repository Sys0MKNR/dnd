import helper.util as util
from game.gamedata import GameData
from states.createChar import CreateChar

class InventoryState():
    def run(self, gamedata):
        print("Welcome to your inventory {0}".format(gamedata.player.name))
        while True:
            print("These are your items:")
            for item in gamedata.player.inventory.items:
                print("* {0} \t--increases {1} by {2}".format(item.name, item.influenced_attribute, item.value))
            print("Type 'quit' or the name of the item you want to use/drop")
            value = input("> ")

            choosenItem = [item for item in gamedata.player.inventory.items if item.name == value]

            if value == "quit":
                break

            if not choosenItem:
                continue

                            
            choosenItem = choosenItem[0]

            print("Do you want to 'use' or 'drop' the {0}? Else 'quit' ".format(choosenItem.name))
            
            value = input("> ")

            if value == 'quit':
                break
            elif value == 'use':
                
                try:
                    oldValue = getattr(gamedata.player.attributes, choosenItem.influenced_attribute)
                    newVAlue = oldValue + gamedata.player.inventory.use(choosenItem)
                    setattr(gamedata.player.attributes, choosenItem.influenced_attribute, newVAlue)
                except AttributeError:
                    oldValue = getattr(gamedata.player, choosenItem.influenced_attribute)
                    newVAlue = oldValue + gamedata.player.inventory.use(choosenItem)
                    setattr(gamedata.player, choosenItem.influenced_attribute, newVAlue)
                
                print("The item was used.")
            elif value == 'drop':
                gamedata.player.inventory.drop(choosenItem)
                print("The item was dropped.")
            else:
                continue
        return gamedata


if __name__ == '__main__':
    gamedata = GameData()
    gamedata.player = util.load_player('p_items.json')
    g = InventoryState().run(gamedata)
    print(g.player.attributes.strength)
    print(g.player.inventory.items)