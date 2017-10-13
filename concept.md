max inventory space: 20
von gear kann nur eines einer art getragen werden



# Start game and parse attributes and do stuff accordingly

create-player: spieler erstellen
savefile: savefile verwenden
kein parameter: usage ausgeben


bei createplayer spieler erstellen
bei savefile: validaten und dann ins dorf. 
das dorf ist der main Statehandler



## Create a Character
* Start
* Strength
* Agility
* Speed
* Defense
* Confirm
* Store

## Village
* Start
* List
* Choose
* Save
* Quit

## Dungeon
* Start
* Look
* Move
* Open
* Fight
* Attack
* Inventory
* Menu
* Success
* Exit

## Villager
* Start
* List
* Choose




# villager

#name
* action(buy, sell, process)
* welcometext
* errortext
* choosentext

## ablauf

1. welcome
2. list items
3. choose item
4. success/error
5. restart




# fight

mehrere Gegner Typen
    orc(20-30)
    witch(40-60)
    human(30-40)
    nord(35-45)
    nazi-zombie(40-50)
    unicorn(50-60)

speed entscheidet wer als erstes angreift

agility: 
    doppelt so viel agility wie gegner 50 % ausweichwahrscheinlichkeit
    3 mal so viel 100% 
    
    (200 - 2 )/22

strength == schaden

defense == schadensresistennz => tatsächlicher schaden = strength - defense

defense wird jede rund um 25% weniger