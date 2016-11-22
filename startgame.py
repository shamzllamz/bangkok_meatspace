# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#fun stuff
import cmd, sys, textwrap
import time
import random
import os
import ctypes

import turnoff

title_banner = """
           d8888b.  .d8b.  d8b   db  d888b  db   dD  .d88b.  db   dD
           88  `8D d8' `8b 888o  88 88' Y8b 88 ,8P' .8P  Y8. 88 ,8P'
           88oooY' 88ooo88 88V8o 88 88      88,8P   88    88 88,8P
           88~~~b. 88~~~88 88 V8o88 88  ooo 88`8b   88    88 88`8b
           88   8D 88   88 88  V888 88. ~8~ 88 `88. `8b  d8' 88 `88.
           Y8888P' YP   YP VP   V8P  Y888P  YP   YD  `Y88P'  YP   YD


  .88b  d88. d88888b  .d8b.  d888888b .d8888. d8888b.  .d8b.   .o88b. d88888b
  88'YbdP`88 88'     d8' `8b `~~88~~' 88'  YP 88  `8D d8' `8b d8P  Y8 88'
  88  88  88 88ooooo 88ooo88    88    `8bo.   88oodD' 88ooo88 8P      88ooooo
  88  88  88 88~~~~~ 88~~~88    88      `Y8b. 88~~~   88~~~88 8b      88~~~~~
  88  88  88 88.     88   88    88    db   8D 88      88   88 Y8b  d8 88.
  YP  YP  YP Y88888P YP   YP    YP    `8888Y' 88      YP   YP  `Y88P' Y88888P
"""

def clrScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def waitForInput(message):
    try:
        raw_input(message)
    except SyntaxError:
        pass

def ErrorMessage(text):
    print(" AN ERROR HAS OCCURRED.")
    print("\n")
    ctypes.windll.user32.MessageBoxA(0, text, "ERROR", 0x30)

def AccessDenied():
    print(" ERROR: INCORRECT AUTHENTICATION")
    print("\n")
    ctypes.windll.user32.MessageBoxA(0, "ACCESS DENIED", "ERROR", 0x00000010L)

def getAllItemsMatchingDesc(desc, itemList):
    itemList = list(set(itemList)) # make itemList unique
    matchingItems = []
    for item in itemList:
        if desc in items[item].descwords:
            matchingItems.append(item)
    return matchingItems

def getFirstItemMatchingDesc(desc, itemList):
    itemList = list(set(itemList))  # make itemList unique
    for item in itemList:
        try:
            if desc in items[item].descwords:
                return item
        except KeyError:
            if desc in npcs[item].descwords:
                return item
        except:
            if desc in rooms[item].descwords:
                return item
    return None

def getFirstLocMatchingDesc(desc, itemList):
    itemList = list(set(itemList))
    for item in itemList:
        if desc in rooms[item].descwords:
            return item
    return None

def getFirstPersonMatchingDesc(desc, itemList):
    itemList = list(set(itemList))
    for item in itemList:
        if desc in npcs[item].descwords:
            return item
    return None

class Player:
    def __init__(self):
        self.status = []
        self.health = 30
        self.maxhealth = 30
        self.alive = True
        self.strength = 50
        self.maxstrength = 50
        self.perception = 50
        self.hunger = 15
        self.energy = 140
        self.maxenergy = 200
        self.inv = ["hand", "cigarettes"]
        self.authentications = []
        self.currentRoom = None
        self.system = {}
        self.money = random.randint(100, 1000)

    def status_effects(self):
        for item in player.system:
            player.system[item] -= 5
    def checkHunger(self):
        hunger_messages = ["hungry", "very hungry", "starving", "full", "very full"]
        if "wired" in self.status:
            self.hunger += 1
        elif "exhausted" in self.status:
            self.hunger += random.randrange(8, 12)
        elif "very tired" in self.status:
            self.hunger += random.randrange(7, 9)
        elif "tired" in self.status:
            self.hunger += random.randrange(4, 6)
        else:
            self.hunger += random.randrange(3)
        if self.hunger >= 100:
            if "starving" not in self.status:
                for item in hunger_messages:
                    if item in self.status:
                        self.status.remove(item)
                self.status.append("starving")
                print("You begin to starve.")
        elif self.hunger >= 80:
            if "very hungry" not in self.status:
                for item in hunger_messages:
                    if item in self.status:
                        self.status.remove(item)
                self.status.append("very hungry")
                print("You are very hungry!")
        elif self.hunger >= 60:
            if "hungry" not in self.status:
                for item in hunger_messages:
                    if item in self.status:
                        self.status.remove(item)
                self.status.append("hungry")
                print("You feel hungry.")
        elif self.hunger < -10:
            if "very full" not in self.status:
                for item in hunger_messages:
                    if item in self.status:
                        self.status.remove(item)
                self.status.append("very full")
                print("You let out a burp. It was difficult to not let anything else get out.")
        elif self.hunger < 5:
            if "full" not in self.status:
                for item in hunger_messages:
                    if item in self.status:
                        self.status.remove(item)
                self.status.append("full")
                print("You let out a burp.")
        # checks if player is not actually hungry
        else:
            if self.hunger < 60 and self.hunger >= 0:
                for item in hunger_messages:
                    if item in self.status:
                        self.status.remove(item)

    def checkEnergy(self):
        energy_messages = ["wired", "tired", "very tired", "exhausted"]
        if self.energy <= -20:
            self.pass_out()
        elif self.energy <= 0:
            if "exhausted" not in self.status:
                for item in energy_messages:
                    if item in self.status:
                        self.status.remove(item)
                self.status.append("exhausted")
                print("You are exhausted!")
        elif self.energy <= self.maxenergy/8:
            if "very tired" not in self.status:
                for item in energy_messages:
                    if item in self.status:
                        self.status.remove(item)
                self.status.append("very tired")
                print("You are very tired.")
        elif self.energy <= self.maxenergy/2:
            if "tired" not in self.status:
                for item in energy_messages:
                    if item in self.status:
                        self.status.remove(item)
                self.status.append("tired")
                print("You feel tired.")
        elif self.energy > self.maxenergy:
            if "wired" not in self.status:
                for item in energy_messages:
                    if item in self.status:
                        self.status.remove(item)
                self.status.append("wired")
                print("You feel wired!")
        else:
            if self.energy > self.maxenergy/2 and self.energy <= self.maxenergy:
                for item in energy_messages:
                    if item in self.status:
                        self.status.remove(item)

    def expendEnergy(self, mode_of_expenditure):
        if "very hungry" in self.status:
            self.expenditure_dict = {"goto" : 10, "about": 4, "get" : 5, "buy" : 7, "wait" : 2, "list" : 4, "talkto" : 9}
        else:
            self.expenditure_dict = {"goto" : 5, "about": 2, "get" : 3, "buy" : 4, "wait" : 1, "list" : 2, "talkto" : 4}
        self.expenditure = self.expenditure_dict[mode_of_expenditure]
        # if player has too little energy
        if self.expenditure > self.energy:
            self.hunger += 10       # gives player some hunger
        self.energy -= self.expenditure
    # one function to run to check all the player's vitals (hunger, energy, etc)
    def checkVitals(self):
        self.status_effects()
        self.checkHunger()
        self.checkEnergy()
        if player.hunger >= 100:
            player.take_damage(2)
        if player.health <= 0:
            self.die()
        # print("Current health: %s" %player.health)  # for debug purposes
        # print("Current energy: %s" %player.energy) # for debug purposes
        # print("Current hunger: %s" %player.hunger)  # for debug purposes
        # print("Current statuses: %s" %player.status) # for debug purposes

    def goto(self, direction):
        if direction != "exit":
            list = self.currentRoom.subdirectories
            destination = getFirstLocMatchingDesc(direction, list)
            if destination == None :
                print("You cannot see that directory.")
                print("\n")
            else:
                if rooms[destination].name in self.authentications:
                    self.expendEnergy("goto")
                    clrScreen()
                    #  HERE:   add randomized message for each room after goto verb is used
                    self.currentRoom = rooms[destination]
                    self.look()
                    self.currentRoom.playervisits += 1
                else:
                    AccessDenied()
        elif direction == "exit":
            self.exit()
    def exit(self):
        if self.currentRoom.up != False:
            self.expendEnergy("goto")
            destination = self.currentRoom.up
            clrScreen()
            self.currentRoom = rooms[destination]
            self.look()
        else:
            print("You cannot see an exit here.")
            print("\n")

    def look(self):
        list = []
        xcounter = self.currentRoom.up
        slugline = "\n12B / "
        while (xcounter != False):
            list.append(rooms[xcounter].name)
            xcounter = rooms[xcounter].up
        list.reverse()
        for item in list:
            slugline += item + " / "
        slugline += self.currentRoom.name
        print(slugline)
        print("\n")
        for item in self.currentRoom.descriptions:
            print("\n".join(textwrap.wrap(item, SCREEN_WIDTH)))
            print("\n")
        self.list("directory")
        self.list("subdirectories")
        # atmosphere
    def examine(self, object):
        self.expendEnergy("about")
        enoughPerception = True     # for rolling against player perception (determine later)

        if object == "me":
            if player.alive:
                print("VITAL SIGNS PRESENT")
            print("Health: %s/%s" %(self.health, self.maxhealth))
            print("Energy: %s/%s" %(self.energy, self.maxenergy))
            print("Hunger: %s" %self.hunger)
            print("Strength: %s/%s" %(self.strength, self.maxstrength))
            print("\n")
            return

        # see if object is in player's current room
        item = getFirstItemMatchingDesc(object, self.currentRoom.directory)
        if item != None:
            print("\n")
            try:
                print("\n".join(textwrap.wrap(items[item].longdesc, SCREEN_WIDTH)))
                print("\n")
                return
            except KeyError:
                print("\n".join(textwrap.wrap(npcs[item].description, SCREEN_WIDTH)))
                print("\n")
                return

        # see if object is in current room's subdirectories
        item  = getFirstLocMatchingDesc(object, self.currentRoom.subdirectories)
        if item != None:
            print("\n")
            print("\n".join(textwrap.wrap(rooms[item].descriptions[0], SCREEN_WIDTH)))
            print("\n")
            return

        item = getFirstItemMatchingDesc(object, self.currentRoom.shop)
        if item != None:
            print("\n")
            print("\n".join(textwrap.wrap(items[item].longdesc, SCREEN_WIDTH)))
            print("\n")
            return

        # see if object is in player's inventory
        item = getFirstItemMatchingDesc(object, self.inv)
        if item != None:
            print("\n")
            print("\n".join(textwrap.wrap(items[item].longdesc, SCREEN_WIDTH)))
            print("\n")
            return
        # if none of the above
        print("You don't see that nearby.")
        print("\n")
    def list(self, obj):
        self.expendEnergy("list")
        # prints list of subdirectories, if possible
        if obj == "subdirectories":
            if self.currentRoom.subdirectories != []:
                print("\nAvailable subdirectories: ")
                for item in self.currentRoom.subdirectories:
                    print("    %s" %rooms[item].name)
            if self.currentRoom.up != False: print("\nExit to: %s" % rooms[self.currentRoom.up].name)
            print("\n")
        # print list of objects in current directory, else display "There is nothing here."
        elif obj == "directory":
            if self.currentRoom.directory != []:
                for item in (self.currentRoom.directory):
                    try:
                        if items[item].prose == False:
                            if items[item].plural == False:
                                if items[item].shortdesc[0] in {'a','e','i','o','u'}:
                                    print("There is an %s here." %items[item].shortdesc)
                                else:
                                    print("There is a %s here." %items[item].shortdesc)
                            else:
                                print("There are some %s here." %items[item].shortdesc)
                    except KeyError:
                        print("\n".join(textwrap.wrap(npcs[item].shortdesc[0])))
                        print("\n")
                        if self.currentRoom.playervisits < 1:
                            for i in npcs[item].shortdesc[1:]:
                                print("\n".join(textwrap.wrap(i)))
                                print("\n")
            # elif self.currentRoom.directory == []:
            #     print("There is nothing here.")
        # list inventory
        elif obj == "inventory":
            self.checkinv()
        elif obj == "prices":
            self.checkPrices()
        else:
            print("You can't find that list.")
    def checkinv(self):
        print("\n")
        # checks if inventory is empty
        if self.inv == []:
            print("You don't have anything on you.")
            print("\n")

        # if player has items in inventory
        else:
            print("You have:")
            for i in self.inv:
                if items[i].plural == False:
                    if i[0] in ('a', 'e', 'i', 'o', 'u'):
                        print("an %s" %items[i].shortdesc)
                    else:
                        print("a %s" %items[i].shortdesc)
                else:
                    print("some %s" %items[i].shortdesc)
            if self.money > 0:
                print("%s RMB" %self.money)
            elif self.money <= 0:
                print("You have no money.")
            print("\n")
    def checkPrices(self):
        prices = {}
        list = []
        for item in player.currentRoom.shop:
            if items[item].price:
                prices[items[item].name] = items[item].price
        if prices != {}:
            print("\n")
            for x in prices:
                print("%s:    %s RMB" %(x, prices[x]))
            print("\n")
        elif prices == {}:
            print("There is nothing for sale here.")
            print("\n")

    def get(self, itemToTake):
        tooHeavy = False
        item = getFirstItemMatchingDesc(itemToTake, self.currentRoom.directory)
        if item != None:
            # checks if the item is takeable
            if items[item].takeable[0] == False:
                # see if item has custom message to prevent player from taking it
                try:
                    print(items[item].takeable[1])
                    print("\n")
                # otherwise print generic message
                except:
                    print("You don't want the %s." %items[item].shortdesc)
                    print("\n")
            # if the item weighs too much for the player to carry
            elif items[item].weight > self.strength:
                print("You don't have enough strength for the %s." %items[item].shortdesc)
            # if item is takeable AND not too heavy
            else:
                self.currentRoom.directory.remove(item)
                self.inv.append(item)
                self.expendEnergy("get")
                print("Gotten: %s" %items[item].shortdesc)
                print("\n")
        else:
            if itemToTake[0] in {'a','e','i','o','u'}:
                print("You don't see an %s here." %itemToTake)
                print("\n")
            else:
                print("You don't see a %s here." %itemToTake)
                print("\n")
    def drop(self, itemToDrop):
        item = getFirstItemMatchingDesc(itemToDrop, self.inv)
        if item != None:
            if item == "hand":
                print("You are quite attached to it.")
                print("\n")
            else:
                self.inv.remove(item)
                items[item].prose = False
                self.currentRoom.directory.append(item)
                print('You drop the %s.' % items[item].shortdesc)
                print("\n")
        else:
            if itemToDrop[0] in {'a','e','i','o','u'}:
                print("You don't have an %s to drop." %itemToDrop)
                print("\n")
            else:
                print("You don't have a %s to drop." %itemToDrop)
                print("\n")
    def eat(self, object):
        item = getFirstItemMatchingDesc(object, self.inv)
        # checks if item exists
        if item != None:
            # checks if item is edible
            if items[item].edible == True:
                self.inv.remove(item)
                print("You eat the %s." %items[item].shortdesc)
                print("\n")
                if items[item].nutrition != None:
                    self.hunger -= items[item].nutrition
            # if item is not edible
            else:
                print("You can't eat that!")
                print("\n")
        # if can't find item
        else:
            if object[0] in {'a', 'e', 'i', 'o', 'u'}:
                print("You don't have an %s." %object)
                print("\n")
            else:
                print("You don't have a %s." %object)
                print("\n")
    def drink(self, object):
        item = getFirstItemMatchingDesc(object, self.inv)
        # check if item exists
        if item != None:
            # check if item is drinkable
            if items[item].drinkable:
                self.inv.remove(item)
                print("You drink the %s." %items[item].shortdesc)
                print("\n")
                if items[item].nutrition:
                    self.hunger -= items[item].nutrition
                if items[item].energy:
                    self.energy += items[item].energy

            else:
                print("You cannot drink that.")
                print("\n")
        else:
            if object[0] in {'a', 'e', 'i', 'o', 'u'}:
                print("You don't have an %s to drink." %object)
                print("\n")
            else:
                print("You don't have a %s to drink." %object)
                print("\n")
    def smoke(self, object):
        item = getFirstItemMatchingDesc(object, self.inv)
        if item != None:
            if items[item].smokeable:
                self.inv.remove(item)
                print("You smoke a %s." %items[item].shortdesc)
                print("\n")
                if items[item].nicotine:
                    # if player doesn't already have nicotine in system, add full nicotine
                    if "nicotine" not in self.system:
                        self.hunger -= items[item].nicotine
                        self.system["nicotine"] = items[item].nicotine
                    # if the player already has less than five nicotine in system, add half of nicotine
                    elif self.system["nicotine"] <= 5:
                        self.hunger -= int(items[item].nicotine / 2)
                if items[item].energy:
                    self.energy += items[item].energy
            else:
                print("You can't smoke that!")
                print("\n")
        else:
            if object[0] in {'a', 'e', 'i', 'o', 'u'}:
                print("You don't have an %s." %object)
                print("\n")
            else:
                print("You don't have a %s." %object)
                print("\n")
    def buy(self, object):
        item = getFirstItemMatchingDesc(object, self.currentRoom.shop)
        try:
            price = items[item].price
        except:
            print("That item is not for sale.")
            print("\n")
            return
        if player.money >= price:
            self.expendEnergy("buy")
            player.money -= price
            player.inv.append(item)
            if items[item].plural == False:
                if item[0] in {'a','e','i','o','u'}:
                    print("You buy an %s." %items[item].shortdesc)
                else:
                    print("You buy a %s." %items[item].shortdesc)
            else:
                print("You buy some %s." %items[item].shortdesc)
            print("\n")
            items[item].bought()
        else:
            self.expendEnergy("buy")
            print("Insufficient funds.")
            print("\n")
    def talkto(self, object):
        npc = getFirstItemMatchingDesc(object, self.currentRoom.directory)
        try:
            person = npcs[npc]
            if person != None:
                self.expendEnergy("talkto")
                if person.talkedTo == False:
                    person.talkedTo = True
                    print("\n".join(textwrap.wrap(person.speech[0], SCREEN_WIDTH)))
                    print("\n")
                    person.talk()
                elif person.talkedTo == True:
                    if person.speech[1]:
                        print("\n".join(textwrap.wrap(person.speech[1], SCREEN_WIDTH)))
                        print("\n")
                    else:
                        print(person.speech[0])
        except:
            print("There is no %s here." %object)
            print("\n")

    def wait(self):
        # should replace with function that randomized "time passes" and room-specific messages
        self.expendEnergy("wait")
        print("Time passes.")
        print("\n")
    def sleep(self):
        if self.currentRoom.name == "CHEAP HOTEL":
            if player.money >= 30:
                print("It's been a long day. Time to go to sleep.")
                print("\n")
                waitForInput("Press [Enter] to continue...")
                turnoff.turnOffScreen()
                clrScreen()
                self.money -= 30
                self.energy = self.maxenergy - 20
                self.hunger += 12
                print("\n".join(textwrap.wrap("You wake up with a little difficulty. At this point, your nightmares are no longer nightmares.", SCREEN_WIDTH)))
                print("\n")
            else:
                print("You can't afford another night at Cheap Hotel.")
                print("Your heart flutters in a small moment of panic.")
                print("\n")
        else:
            print("It's not safe to sleep anywhere but home.")
            print("\n")
    def pass_out(self):
        print("\n".join(textwrap.wrap("You try to muster the last of your strength, but it's too much. Your legs give out, and you collapse.", SCREEN_WIDTH)))
        print("Oh, sweet unconsciousness.")
        print("\n")
        waitForInput("Press [Enter] to continue...")
        turnoff.turnOffScreen()
        clrScreen()
        self.energy = self.maxenergy/2
        self.hunger += 25
    def take_damage(self, dmg):
        self.health -= dmg
    def die(self):
        self.alive = False


class Location:
    def __init__(self):
        self.name = ""      # name of the location
        self.descriptions = []     # list of descriptions of the location
        self.up = False # when the player goes 'back' or 'exit'
        self.subdirectories = []
        self.directory = []    # list of objects in the location
        self.events = {}    # dictionary of events that will happen over turns
        self.playervisits = 0   # how many times the player has visited the location
        self.descwords = []
        self.exitmessage = ""
        self.shop = []
    def execute_event(self):
        self.playervisits += 1
        if self.playervisits in self.events:
            print(self.events[self.playervisits])
    def authenticate_player(self):
        player.authentications.append(self.name)

class DarkAlley(Location):
    def __init__(self):
        Location.__init__(self)
        self.name = "DARK ALLEY"
        self.descwords = ["dark", "alley"]
        self.descriptions = ["The alleyway is dark. Somewhere in the city, the air pressure drops, and litter scuttles across the ground accordingly.", "Police blimps cruise over the rooftops, trawling the alleys with spotlights. One lands on you. You raise your hand to shield your eyes, but it's already gone.", "There is nothing here."]
        self.up = "jed yod"
        self.events = {1:"[Command: type 'goto exit']"}
        self.authenticate_player()

class SmallAlley(Location):
    def __init__(self):
        Location.__init__(self)
        self.name = "SMALL ALLEY"
        self.descwords = ["small", "alley"]
        self.descriptions = ["This small alleyway past the parking complex would be unnoticeable in the clutter of the Bazaar but for the red CHEAP HOTEL, neon-lit down the length of the adjacent building.", "A familiar passageway leads to the elevator of the Hotel. Across from it, a massage parlor advertises: 24 HOURS - REAL THAI. The windows above glow with a pink magenta."]
        self.up = "night bazaar"
        self.subdirectories = ["cheap hotel", "thai massage"]
        self.events = {}
        self.authenticate_player()

class CheapHotel(Location):
    def __init__(self):
        Location.__init__(self)
        self.name = "CHEAP HOTEL"
        self.descwords = ["cheap", "hotel"]
        self.descriptions = ["It's not much, but it's home. For 30 RMB a night, at least.", "Your coffin consists of a futon, which takes most of your so-called floorspace, and some storage shelves above. A single LED strip overhead reflects off the sterile, stain-resistant walls."]
        self.up = "small alley"
        self.directory = ["shelves", "led strip", "futon"]
        self.authenticate_player()

class ThaiMassage(Location):
    def __init__(self):
        Location.__init__(self)
        self.name = "THAI MASSAGE PARLOR"
        self.descwords = ["thai","massage","parlor"]
        self.descriptions = ["A line of old leather chairs seat a handful of patrons, their feet protruding from the bamboo partitions between them. Chattering masseuses busy themselves, a bottle of oil always in reach."]
        self.up = "small alley"
        self.directory = ["madam"]
        self.shop = ["foot massage", "special massage"]
        self.subdirectories = ["private area"]
        self.authenticate_player()

class JedYod(Location):
    def __init__(self):
        Location.__init__(self)
        self.name = "JED YOD DISTRICT"
        self.descwords = ["jed", "yod"]
        self.descriptions = ["In better times, the streets would be resplendent with a tapestry of neon. But the Migration happened, and then the Quarantine hit. Now what's left is just a patchwork of its original splendor.", "The corporate monoliths of Silom loom in the distance, some piercing the sky to reach the Metropolis above. On the horizon, you catch a glimpse of the Wasteland's edge, where silent fireballs bloom."]
        self.directory = ["protester"]
        self.subdirectories = ["ftp station", "temple", "night bazaar", "dark alley"]
        self.authenticate_player()

class NightBazaar(Location):
    def __init__(self):
        Location.__init__(self)
        self.name = "NIGHT BAZAAR"
        self.descwords = ["night", "bazaar"]
        self.descriptions = ["The Bazaar is the one place in the Sector that doesn't seem to be affected by the Quarantine. It's business as usual: outdoor vendors crowd the already narrow streets, and the Bazaar's more permanent establishments tower on either side."]
        self.subdirectories = ["anusarn market", "irish pub", "noodle bar", "small alley"]
        self.up = "jed yod"
        self.authenticate_player()

class AnusarnMarket(Location):
    def __init__(self):
        Location.__init__(self)
        self.name = "ANUSARN MARKET"
        self.descwords = ["anusarn", "market"]
        self.descriptions = ["A remnant of the Old World, still thriving with activity. The cries of vendors, their wares glittering on a sea of synthetic fabrics, mingles with sizzling meat in the air."]
        self.up = "night bazaar"
        self.shop = ["synthmeat sausage", "fried insects", "plastic bracelet", "street coffee"]
        self.directory = ["hawkers"]
        self.authenticate_player()

class IrishPub(Location):
    def __init__(self):
        Location.__init__(self)
        self.name = "IRISH PUB"
        self.descwords = ["irish", "pub"]
        self.descriptions = ["A cut-and-paste pub from when Ireland was still a thing. The decor is a tacky green."]
        self.up = "night bazaar"
        self.directory = ["bartender"]
        self.shop = ["stew", "guidness"]
        self.authenticate_player()

class NoodleBar(Location):
    def __init__(self):
        Location.__init__(self)
        self.name = "NOODLE BAR"
        self.descwords = ["noodle", "bar"]
        self.descriptions = ["A small but brightly lit noodle bar on the side of the road. The type of place that does one thing, and one thing only. But it does it well.", "Steam rises from the simmering broth."]
        self.up = "night bazaar"
        self.shop = ["boat noodles"]
        self.authenticate_player()

class FTPJedYod(Location):
    def __init__(self):
        Location.__init__(self)
        self.name = "FTP STATION"
        self.descwords = ["ftp", "station"]
        self.descriptions = ["The free transit network is the city's arteries, affording commuters rapid access to other districts in the intricate clockwork of the urban system."]
        self.directory = ["transients", "vending machine"]
        self.up = "jed yod"
        self.shop = ["coca cola", "cup noodles", "energy bar"]
        self.authenticate_player()

class Temple(Location):
    def __init__(self):
        Location.__init__(self)
        self.name = "TEMPLE"
        self.descwords = ["wat", "temple"]
        self.descriptions = ["The entrance of the temple is guarded by two grotesques, figures of naked women dangling from their fanged mouths. They stare from their perches on either side of the gate."]
        self.up = 'jed yod'
        self.subdirectories = ["ordination hall", "chedi", "teaching hall", "archive"]
        self.authenticate_player()

class OrdinationHall(Location):
    def __init__(self):
        Location.__init__(self)
        self.name = "ORDINATION HALL"
        self.descwords = ["ordination", "hall", "ubosot", "bot"]
        self.descriptions = ["The ordination hall is the holist part of the temple, apart from the reliquary tower. Used for religious rituals and ceremonies, it is forbidden for women or other vulgarities to enter."]
        self.up = "temple"

class Chedi(Location):
    def __init__(self):
        Location.__init__(self)
        self.name = "CHEDI"
        self.descwords = ["chedi", "reliquary", "tower", "stupa"]
        self.descriptions = ["A gargantuan mound with a spire that juts into the sky. The reliquary tower is the most sacred building of the monastery, said to contain a part of the Buddha himself."]
        self.up = "temple"

class TeachingHall(Location):
    def __init__(self):
        Location.__init__(self)
        self.name = "TEACHING HALL"
        self.descwords = ["teaching", "hall", "viharn"]
        self.descriptions = ["The hall is cavernous, richly decorated with murals and carved figures. At the end of the hall presides a larger-than-life golden Buddha, haloed by an eight-spoked wheel."]
        self.directory = ["monk"]
        self.up = "temple"
        self.authenticate_player()

class Archive(Location):
    def __init__(self):
        Location.__init__(self)
        self.name = "ARCHIVE"
        self.descwords = ["archive"]
        self.descriptions = ["A small building at the back of the temple compound, raised on stilts above a large pond. Two banks of outdated monitors inside comprise the temple archive."]
        self.directory = ["scholar"]
        self.up = "temple"
        self.authenticate_player()

class SilomRoad(Location):
    def __init__(self):
        Location.__init__(self)
        self.name = "SILOM ROAD"
        self.descwords = ["silom", "road"]
        self.descriptions = []
        self.up = 'jed yod'
        self.authenticate_player()

class PrivateArea(Location):
    def __init__(self):
        Location.__init__(self)
        self.name = "PRIVATE AREA"
        self.descwords = ["private", "area"]
        self.descriptions = ["What happens in the private area stays in the private area. That much is known.", "The bead curtains clatter and you follow a narrow, winding passageway. After a few turns, you gradually lose all sense of direction.", "The hall finally terminates in a room, just tall enough to stand in. A bare bulb hangs above a lonely wooden chair at the center, and reflects off the mirrors that cover the three walls which don't contain a doorway.", "There is nothing here."]
        self.up = 'thai massage'


class NPC:
    def __init__(self):
        self.name = ""
        self.shortdesc = []
        self.description = ""
        self.descwords = []
        self.speech = []
        self.talkedTo = False
    def talk(self):
        pass

class Monk(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.name = "Monk"
        self.shortdesc = ["A MONK is here. He sits cross-legged, meditating with eyes closed.", "A small diode on his temple glows hypnotically in the dimness of the room."]
        self.speech = ["You decide not to disturb his meditation."]
        self.description = "The iconic saffron robe is recognizable anywhere. This particular monk has a neuroprosthesis -- you can tell by the blinking diode on his temple -- undoubtedly from KITTECH, who sponsored the building of the Archive."
        self.descwords = ["monk"]

class Scholar(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.name = "Scholar"
        self.shortdesc = ["There is a SCHOLAR sitting at one of the terminals, browsing the Archives. You can tell from the way she dresses that she's not from around here. A Metropolitan, from the looks of it -- or trying hard to pose as one.", "She looks up at your intrusion, and then her attention is back on the screen again."]
        self.speech = ["'Do you know when the quarantine will be lifted?' she asks. 'I need to get back to Silom in time for the last blimp.'", "'There's something happening upstairs,' she says cryptically. Then it's back to the books for her."]
        self.description = "The Scholar exudes softness: from her posture to the woolen fibers of her clothing. The extraneous elements such as the tie that hangs from her neck indicate she's never experienced the hard streets of New Bangkok."
        self.descwords = ["scholar", 'student']

class Protester(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.name = "Protester"
        self.shortdesc = ["The streets are deserted. A lone PROTESTER holds up a cardboard sign. 'Our streets don't belong to the machines!' he cries into the void.", "Foolish man. Ever since the automobile, the streets have always belonged to the machines."]
        self.descwords = ["protester", "protestor"]
        self.description = "His tattered clothing indicates he's from the Wastelands."
        self.speech = ["Happy to prosthelytize, he steps forward to give you something. Then he sees your hand, and he shrinks away. A piece of paper flutters to the ground.", "He avoids your eyes, nervously crossing to the other side of the road."]
    def talk(self):
        player.currentRoom.directory.append("leaflet")

class Madam(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.name = "Madam"
        self.shortdesc = ["The MADAM sits at a counter. She eyes you dubiously.", "'Can I help you?' she asks."]
        self.descwords = ["madam"]
        self.description = "A middle-aged woman with a practiced calm. Her beady eyes see everything, it seems."
        self.speech = ["'Foot massages are seventy a pop,' she says. 'Special private massages for two hundred. Respectable customers only.' A pointed look at your hand."]

class Hawkers(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.name = "Hawkers"
        self.shortdesc = ["There are hawkers here, selling street food from their carts. Some things never change."]
        self.descwords = ["hawkers", "vendors", "hawker"]
        self.description = "Although the carts they hawk from are impermanent by nature, they look like they've inhabited the same little space for years."
        self.speech = ["'Crickets! Grasshoppers! Jewelry for your special ones!'"]

class Bartender(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.name = "Bartender"
        self.shortdesc = [ "The BARTENDER smiles at you expectantly.", "'Hey, you.' He gives you a knowing wink. 'I know a guy'."]
        self.descwords = ["bartender"]
        self.description = "A man with a relaxed demeanor. He doesn't seem at all concerned with the apparent lack of customers as he jovially wipes the countertops for the umpteenth time."
        self.speech = ["'You wanna get on one of those blimps?' he jabs his finger in the air, at something beyond the ceiling. 'I can get you a ticket. Really cheap: three hundred thousand RMB.'"]

class Transients(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.name = "Transients"
        self.shortdesc = ["The lines are closed due to the quarantine measures, but the usual transients are present. They huddle around a trash can fire."]
        self.description = "The quarantine hit everybody hard, augs and non-augs alike. In fact, it probably hit augs the hardest. Many were run out of their homes, their prosthetics hidden under coatsleeves."
        self.speech = ["'Got any food?'"]
        self.descwords = ['transient', 'transients', 'hobo', 'hobos', 'homeless']



class Item:
    def __init__(self):
        self.name = ""
        self.shortdesc = ""         # short description of the item (eg in inventory list)
        self.longdesc = ""          # long description of the item (when the player examines item)
        self.takeable = (True,)     # in a tuple because if False, then following values will be the messages returned to the user
        self.descwords = []         # list of words to describe item (for parser)
        self.weight = 10            # weight of item (might use for rolling against character strength)
        self.casts_light = False    # does the item cast light? (default = false)
        self.edible = False         # might implement eating
        self.drinkable = False      # drinking too maybe
        self.plural = False         # is the item an items? (for the parser)
        self.prose = True           # is the item already described in the prose? (affects if showLocation() prints additional lines for this item)
        self.nutrition = None       # if the item is eaten, how much hunger does it satiate?
        self.smokeable = False      # gonna smoke some stuff
        self.energy = None          # does the item give the player energy?
    def bought(self):
        pass

class VendingMachine(Item):
    def __init__(self):
        Item.__init__(self)
        self.name = "vending machine"
        self.shortdesc = "vending machine"
        self.longdesc = "It takes your money and dispenses manufactured consumables. A vending machine."
        self.descwords = ["vending", "machine"]
        self.weight = 500
        self.prose = False

class Hand(Item):
    def __init__(self):
        Item.__init__(self)
        self.name = "BioHand(tm)"
        self.shortdesc = "hand"
        self.longdesc = "You've had it for as long as you can remember. Nothing was cheap back then, not even Chinese knockoffs. It creaks and whines a little now, but it's served you well."
        self.descwords = ["hand"]
        self.prose = False

class Leaflet(Item):
    def __init__(self):
        Item.__init__(self)
        self.shortdesc = "Humanist tract"
        self.descwords = ["leaflet", "tract", "humanist", "paper"]
        self.longdesc = "Militant Humanist literature that describes a life in the Wastelands like a spa vacation from the perils of technology. Its words are regular ink blotches, as if it was pressed manually instead of laser printed."
        self.prose = False
        self.edible = True
        self.nutrition = 1

class Shelves(Item):
    def __init__(self):
        Item.__init__(self)
        self.shortdesc = "shelves"
        self.longdesc = "They contain nothing but dust."
        self.descwords = ["storage", "shelves"]
        self.takeable = (False, "The shelves are built into the walls of the coffin.")
        self.prose = True

class LEDStrip(Item):
    def __init__(self):
        Item.__init__(self)
        self.shortdesc = "LED strip"
        self.longdesc = "The long rectangle of white light reminds you of ancient fluorescents."
        self.descwords = ["LED", "strip", "led","light"]
        self.takeable = (False, "It's your only light source in this coffin. You're not taking it down.")
        self.prose = True

class Futon(Item):
    def __init__(self):
        Item.__init__(self)
        self.shortdesc = "futon"
        self.longdesc = "It's not the softest mattress, but six months have comfortably contoured it to the shape of your body."
        self.descwords = ["futon", "mattress", "bed"]
        self.takeable = (False, "You decide not to lug the futon around.")
        self.prose = True

class Ananas(Item):
    def __init__(self):
        Item.__init__(self)
        self.shortdesc = "ananas"
        self.longdesc = "It's not the fresh kind. It comes out of a can."
        self.descwords = ["ananas", "pineapple"]
        self.prose = False
        self.edible = True
        self.nutrition = 10
        self.price = 30

class BoatNoodles(Item):
    def __init__(self):
        Item.__init__(self)
        self.name = "BOAT NOODLES"
        self.shortdesc = "bowl of Thai boat noodles"
        self.descwords = ["boat", "noodles", "noodle"]
        self.longdesc = "Brisket and sprouts awash in a thick mixture of broth and what is allegedly pig's blood. Thin rice noodles -- your favorite."
        self.edible = True
        self.price = 68
        self.nutrition = 36

class CupNoodles(Item):
    def __init__(self):
        Item.__init__(self)
        self.name = "CUP NOODLES"
        self.shortdesc = "cup of instant Mama noodles"
        self.descwords = ["cup", "noodles", "mama"]
        self.longdesc = "In the past you would've needed to put in your own hot water. Now, thanks to groundbreaking Japanese technology, you just pull the ripcord and it hydrates itself. Nifty."
        self.edible = True
        self.price = 15
        self.nutrition = 12

class EnergyBar(Item):
    def __init__(self):
        Item.__init__(self)
        self.name = "ENERGY BAR"
        self.shortdesc = "energy bar"
        self.longdesc = "A Mevius-branded brick of compressed oats, chocolate, and synthetic honey. Contrary to its name, you don't feel energized after eating it."
        self.descwords = ["energy", "bar"]
        self.edible = True
        self.price = 17
        self.nutrition = 14

class CocaCola(Item):
    def __init__(self):
        Item.__init__(self)
        self.name = "COCA COLA"
        self.shortdesc = "bottle of Coca Cola"
        self.longdesc = "The swirling white over red is recognizeable anywhere. You anticipate that hiss when you open the bottle."
        self.descwords = ["coca", "cola", "coke"]
        self.drinkable = True
        self.price = 14
        self.nutrition = 2
        self.energy = 3

class Stew(Item):
    def __init__(self):
        Item.__init__(self)
        self.name = "STEW"
        self.shortdesc = "stew"
        self.longdesc = "Potatoes and carrots in a hearty stew of lab-grown lamb broth."
        self.descwords = ["stew"]
        self.edible = True
        self.price = 86
        self.nutrition = 40

class Entire12CourseMeal(Item):
    def __init__(self):
        Item.__init__(self)
        self.name = "TWELVE COURSE MEAL"
        self.shortdesc = "entire twelve course meal"
        self.descwords = ["twelve","course","meal"]
        self.longdesc = "You have always longed for the day you could eat an entire twelve course meal from your pockets."
        self.edible = True
        self.price = 3000
        self.nutrition = 1000

class Pizza(Item):
    def __init__(self):
        Item.__init__(self)
        self.name = "PIZZA"
        self.shortdesc = "pizza"
        self.longdesc = "It's an entire pizza you have in your pockets somehow."
        self.descwords = ["pizza"]
        self.prose = False
        self.edible = True
        self.nutrition = 40
        self.price = 99

class SynthmeatSausage(Item):
    def __init__(self):
        Item.__init__(self)
        self.name = "SYNTHMEAT SAUSAGE"
        self.shortdesc = "synthmeat sausage"
        self.longdesc = "After the cannibal fiasco late last century, synthetic meats have come into fashion. Most meat labs are Metropolis-level, but their products can be found in most markets due to high demand."
        self.descwords = ["synthmeat","sausage"]
        self.edible = True
        self.nutrition = 25
        self.price = 28

class FriedInsects(Item):
    def __init__(self):
        Item.__init__(self)
        self.name = "FRIED INSECTS"
        self.shortdesc = "fried insects"
        self.longdesc = "A deep-fried assortment of insects: bamboo worms, cockroaches, grasshoppers, and even the occasional scorpion."
        self.descwords = ["deep","fried","insects"]
        self.edible = True
        self.nutrition = 25
        self.price = 17
        self.plural = True

class StreetCoffee(Item):
    def __init__(self):
        Item.__init__(self)
        self.name = "STREET COFFEE"
        self.shortdesc = "street coffee"
        self.longdesc = "The grimy tan liquid swirls in a translucent plastic bag full of ice cubes. Sometimes it is better not to know much about Bangkok's so-called street coffee, other than it caffinates the hell out of you."
        self.descwords = ["street","coffee"]
        self.drinkable = True
        self.price = 20
        self.energy = 17

class PlasticBracelet(Item):
    def __init__(self):
        Item.__init__(self)
        self.name = "PLASTIC BRACELET"
        self.shortdesc = "plastic bracelet"
        self.longdesc = "Plastic is forever, as the old saying goes. The bracelet is painstakingly handcrafted by the vendor and his children, from the waste that sometimes overflows from Metropolis above. It is entirely useless."
        self.descwords = ["plastic","bracelet"]
        self.price = 45

class Guidness(Item):
    def __init__(self):
        Item.__init__(self)
        self.name = "GUIDNESS"
        self.shortdesc = "glass of Guidness(tm) beer"
        self.longdesc = "The dark liquid froths over. Legend has it this meal in a glass used be called something else, but the name has been long lost."
        self.descwords = ["beer","guidness"]
        self.drinkable = True
        self.price = 59
        self.nutrition = 15

class Cigarettes(Item):
    def __init__(self):
        Item.__init__(self)
        self.name = "MEVIUS CIGARETTES"
        self.shortdesc = "pack of cigarettes"
        self.longdesc = "A pack of Mevius Blues. It can take the edge off hunger for a while, and gives you a small amount of energy."
        self.descwords = ["pack", "cigarettes", "cigs","cigarette"]
        self.smokeable = True
        self.price = 62
        self.nicotine = 15
        self.energy = 5

class FootMassage(Item):
    def __init__(self):
        Item.__init__(self)
        self.name = "FOOT MASSAGE"
        self.shortdesc = "foot massage"
        self.longdesc = "A thirty-minute massage from the toes to the calves involving strong hands, aromatic oils, and pointy wooden objects in strange configurations."
        self.descwords = ["foot", "massage"]
        self.price = 70
        self.energy = 20
    def bought(self):
        print("\n".join(textwrap.wrap("After seating you, the masseuse gets to work. She's enthusiastic, maybe too much so at times, but the experience is over before you know it. You get up, feeling relaxed and rejuvenated.", SCREEN_WIDTH)))
        print("\n")
        player.energy += self.energy
        player.inv.remove("foot massage")

class SpecialMassage(Item):
    def __init__(self):
        Item.__init__(self)
        self.name = "SPECIAL MASSAGE"
        self.shortdesc = "special massage"
        self.longdesc = "You have no idea what a 'special massage' might entail, but actually you may have some idea."
        self.descwords = ["special", "massage"]
        self.price = 200
    def bought(self):
        print("\n".join(textwrap.wrap("The madam accepts your money and beckons past the beaded curtains to the private area. 'Through there,' she says. 'And be patient.'", SCREEN_WIDTH)))
        print("\n")
        player.authentications.append("PRIVATE AREA")
        player.inv.remove("special massage")



# gameParser object
class gameParser:
    def __init__(self):
        self.GAME_LOOP = 0
        self.intro()
        self.menu_screen()
        self.menu_select()
        # COMMENT THIS OUT WHEN NOT DEBUGGING
        #self.play()
    def addLocations(self):
        global rooms
        rooms = {}
        rooms["jed yod"] = JedYod()
        rooms["dark alley"] = DarkAlley()
        rooms["night bazaar"] = NightBazaar()
        rooms["anusarn market"] = AnusarnMarket()
        rooms["irish pub"] = IrishPub()
        rooms["ftp station"] = FTPJedYod()
        rooms["thai massage"] = ThaiMassage()
        rooms["cheap hotel"] = CheapHotel()
        rooms["small alley"] = SmallAlley()
        rooms["noodle bar"] = NoodleBar()
        rooms["temple"] = Temple()
        rooms["private area"] = PrivateArea()
        rooms["ordination hall"] = OrdinationHall()
        rooms["chedi"] = Chedi()
        rooms["teaching hall"] = TeachingHall()
        rooms["archive"] = Archive()
    def addItems(self):
        global items
        items = {}
        items["shelves"] = Shelves()
        items["led strip"] = LEDStrip()
        items["futon"] = Futon()
        items["hand"] = Hand()
        items["cigarettes"] = Cigarettes()
        items["boat noodles"] = BoatNoodles()
        items["12 course meal"] = Entire12CourseMeal()
        items["cup noodles"] = CupNoodles()
        items["energy bar"] = EnergyBar()
        items["coca cola"] = CocaCola()
        items["stew"] = Stew()
        items["synthmeat sausage"] = SynthmeatSausage()
        items["fried insects"] = FriedInsects()
        items["guidness"] = Guidness()
        items["plastic bracelet"] = PlasticBracelet()
        items["street coffee"] = StreetCoffee()
        items["leaflet"] = Leaflet()
        items["foot massage"] = FootMassage()
        items["special massage"] = SpecialMassage()
        items["vending machine"] = VendingMachine()
    def addNPCs(self):
        global npcs
        npcs = {}
        npcs["protester"] = Protester()
        npcs["madam"] = Madam()
        npcs["hawkers"] = Hawkers()
        npcs["transients"] = Transients()
        npcs["bartender"] = Bartender()
        npcs["monk"] = Monk()
        npcs["scholar"] = Scholar()
    def addPlayer(self):
        global player
        player = Player()
    def locatePlayer(self):
        player.currentRoom = rooms["dark alley"]
    def initialize(self):
        self.addPlayer()
        self.addLocations()
        self.addNPCs()
        self.addItems()
        self.locatePlayer()
    def intro(self):
        clrScreen()
        crawl = []
        crawl.append("The YEAR is 21XX. The world is a slave to efficiency.")
        crawl.append("After a century of fornication, Neuroscience and Machine Learning have given birth to the METROPOLIS. Its human grandsires looked upon it, and saw that it was good.")
        crawl.append("As a gift, it was given the human cities of earth. It razed them and settled on the rubble, erecting towers of iron. Its zeal to pierce the sky was surpassed only by its hunger. The earth was hollowed; its rivers drained. Still none could feed the METROPOLIS.")
        crawl.append("In the bowels of the OLD WORLD, life still crawls among the waste. The smell of burnt meat mingles with ignition fumes. There is a scream in the darkness, but all eyes are cast upward. The last of the MIGRATION is set to depart soon. Transport vessels suspend from their fueling docks, thick cables mooring them to the iron sky.")
        crawl.append("A seat on one of those blimps could fetch a pretty penny. Or a sharper knife.")
        crawl.append("Every move could be your last. The sun is absent, but the neon glows, in the sky above the...")
        crawl.append("But you know what they say is true: Blood is now. Plastic is forever.")
        closer = random.randint(5, 6)
        print("\n")
        for x in crawl[:5]:
            print("\n".join(textwrap.wrap(x, SCREEN_WIDTH)))
            print("\n")
        print("\n".join(textwrap.wrap(crawl[closer], SCREEN_WIDTH)))
        print("\n")
        time.sleep(1)
    def menu_screen(self):
        print("\n")
        var = 2
        print(title_banner)
        print('{:^80}'.format("BANGKOK_MEATSPACE written by SHAMA_NG for AGENTS_AND_INTERFACES version 0.6"))
        print("\n")
        print("\n")
        print('{:^80}'.format("[P]lay"))
        print("\n")
        print('{:^80}'.format("[A]bout"))
        print("\n")
        print('{:^80}'.format("[R]estore"))
        print("\n")
        print('{:^80}'.format("[Q]uit"))
        print("\n")
    def menu_select(self):
        while True:
            option = raw_input(">").lower()
            if option == "p" or option == 'play':
                self.initialize()
                clrScreen()
                self.chapter1()
                player.look()
                self.play()
            elif option == "a" or option == "about":
                self.about()
            elif option == "r" or option == "restore":
                print("Restoring savestates not supported.")
                print("\n")
            elif option == "q" or option == "quit":
                sys.exit()
    def about(self):
        print("\n".join(textwrap.wrap("Written and programmed by Shama Ng  <shamang37@gmail.com>", SCREEN_WIDTH)))
        print("\n".join(textwrap.wrap("Made with Python for Agents and Interfaces, for Nishant, and the third in a series of unfinished games for Jonathan Reus. On the auspicious date of the twenty first of November, two thousand and sixteen.", SCREEN_WIDTH)))
        print("\n")
    def chapter1(self):
        crawl = []
        crawl.append("There's a tap on your head. And then another one.")
        crawl.append("You look up to see the neon-drenched skyline of New Bangkok, and the rain starts to pour. You pull up your hood before too much gets in your hair.")
        crawl.append("It's not real rain, of course. Just condensation on the lower city's iron sky. But it's cold as hell, and it smells like piss.")
        crawl.append("You squint through the torrent, but you don't recognize this subdirectory. You must have been wandering again.")
        print("\n")
        for i in crawl:
            print("\n".join(textwrap.wrap(i, SCREEN_WIDTH)))
            print("\n")
        print("\n")
        waitForInput("Press [Enter] to continue...")
    def play(self):
        while True:
            # mechanism for timed messages, atmosphere
            self.GAME_LOOP += 1
            player.currentRoom.execute_event()

            # check the player's vitals
            player.checkVitals()

            # check if the player is still alive
            if player.alive == True:

                # get the player's next 'move'
                playerCommand = raw_input(">").lower().split()       # .split() breaks input up into list array, eg "go east" --> ['go', 'east']

                try:

                    # if verb is 'goto'
                    if playerCommand[0] == "goto":
                        try:
                            player.goto(playerCommand[1])
                        # if player doesn't provide destination in command
                        except IndexError:
                            ErrorMessage("Use 'goto [destination]'.")

                    # if verb is "about"
                    elif playerCommand[0] == "about":
                        # determine if player is looking at anything specific
                        try:
                            player.examine(playerCommand[1])

                        # if player doesn't provide second word,
                        except IndexError:
                            player.look()

                    # if verb is 'get' or 'take'
                    elif playerCommand[0] == 'get':
                        try:
                            player.get(playerCommand[1])

                        # if player does not provide object to act on
                        except IndexError:
                            ErrorMessage("Use 'get [item]'.")


                    # if verb is 'drop'
                    elif playerCommand[0] == 'drop':
                        try:
                            player.drop(playerCommand[1])

                        except IndexError:
                            ErrorMessage("Use 'drop [item]'.")

                    # if verb is 'list'
                    elif playerCommand[0] == 'list':
                        try:
                            player.list(playerCommand[1])

                        except IndexError:
                            player.list("subdirectories")

                    # if verb is 'buy'
                    elif playerCommand[0] == "buy":
                        try:
                            player.buy(playerCommand[1])
                        except IndexError:
                            ErrorMessage("Use 'buy [item]'.")

                    elif playerCommand[0] == 'talkto':
                        try:
                            player.talkto(playerCommand[1])
                        except IndexError:
                            ErrorMessage("Use 'talkto [item]'.")

                    # if verb is 'eat'
                    elif playerCommand[0] == 'eat':
                        try:
                            player.eat(playerCommand[1])
                        except IndexError:
                            ErrorMessage("Use 'eat [item]'.")


                    # if verb is 'drink'
                    elif playerCommand[0] == 'drink':
                        try:
                            player.drink(playerCommand[1])
                        except IndexError:
                            ErrorMessage("Use 'drink [item]'.")


                    # if verb is 'smoke'
                    elif playerCommand[0] == 'smoke':
                        try:
                            player.smoke(playerCommand[1])
                        except IndexError:
                            ErrorMessage("Use 'smoke [item]'.")


                    # wait command
                    elif playerCommand[0] == 'wait':
                        player.wait()

                    # sleep command
                    elif playerCommand[0] == 'sleep':
                        player.sleep()

                    # help screen
                    elif playerCommand[0] == 'help':
                        print("\n")
                        print("Some useful commands:")
                        print("    goto [direction]")
                        print("    about")
                        print("    about [item or subdirectory]")
                        print("    get [item]")
                        print("    list")
                        print("    list [inventory or prices]")
                        print("    eat [item]")
                        print("    quit")
                        print("\n")
                        print("Consult the 1563 word user manual for further information.")
                        print("\n")

                    elif playerCommand[0] == 'die':
                        player.die()
                        print("\n")
                        #break

                    # if player wants to quit
                    elif playerCommand[0] == 'quit':
                        self.menu_screen()
                        break

                    # if verb is not recognized
                    else:
                        ErrorMessage("Command not recognized. Enter 'help' for some useful commands. Consult user manual for further information.")

                except IndexError:
                    ErrorMessage("Empty command invalid.")

            elif player.alive == False:
                print("\n")
                print(" ********** YOU HAVE DIED ********** ")
                print("[R]estore [S]tart a new game [Q]uit")
                while True:
                    input = raw_input(">")
                    if input == "r" or input == 'restore':
                        print("Restoring savefiles not supported.")
                    elif input == "s" or input == 'start':
                        self.menu_screen()
                        self.menu_select()
                        break
                    elif input == "q" or input == 'quit':
                        sys.exit()



if __name__ == '__main__':

    # set screen width
    SCREEN_WIDTH = 80

    # start the game
    GAME = gameParser()


