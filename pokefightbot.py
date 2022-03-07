import os
import pyautogui as pg
import time as t

# ATTACKS (only edit the 'else' segment)
if os.environ['HOSTNAME'] == 'fedora':
    # don't edit anything here it's useless
    main_pokemon_attack = "fire punch"
    yellow_bar_pos = [(2954, 1270), (2955, 1270), (2956, 1270)]
    end_pos_1 = (3147, 746)
    end_pos_2 = (3147, 766)
    end_pos_3 = (3147, 786)
    tagged_strip1 = (2882, 1335)
    tagged_strip2 = (2883, 1335)
    background_pos = (3305, 1210)
    captcha_pos = (3777, 1233)
    secondary_pokemon_attack = "brutql szing"
elif os.environ['HOSTNAME'] == 'nephty-fedora':
    # don't edit anything here it's useless
    main_pokemon_attack = "fire punch"
    secondary_pokemon_attack = "brutql szing"
    yellow_bar_pos = [(356, 980), (357, 980), (358, 980)]
    end_pos_1 = (529, 478)
    end_pos_2 = (529, 458)
    end_pos_3 = (529, 438)
    tagged_strip1 = (291, 920)
    tagged_strip2 = (292, 920)
    background_pos = (652, 933)
    captcha_pos = (1045, 912)
else:
    # Enter the attack that you want your main (stronger) pokemon to use
    YOUR_MAIN_POKEMON_ATTACK_HERE = ""
    # Enter the attack that your want your secondary (weaker) pokemon to use
    YOUR_SECONDARY_POKEMON_ATTACK_HERE = ""
    main_pokemon_attack = YOUR_MAIN_POKEMON_ATTACK_HERE
    secondary_pokemon_attack = YOUR_SECONDARY_POKEMON_ATTACK_HERE
    # CHANGE THESE VARIABLES so that they match the coordinates on your screen (x, y)
    # Read the README.md if you don't know how to get the coordinates of a pixel on your screen
    yellow_bar_pos = [(0, 0), (0, 0), (0, 0)]   # these are the three coordinates of the yellow bar that stands
                                                # next to a message coming from the bot when you're in a battle.
                                                # these coordinates should look like [(x, y), (x+1, y), (x+2, y)].
                                                # These are the same three pixels as strip1, strip2 & strip3 in the
                                                # pokebot.py script.
    end_pos_1 = (0, 0)                          # this is the position of the :tada: emoji when you win a fight and none
                                                # of your pokemon's levels up. WARNING : this pixel MUST be a red one
    end_pos_2 = (0, 0)                          # this is the position of the :tada: emoji when you win a fight and 1
                                                # of your pokemon's levels up. WARNING : this pixel MUST be a red one
    end_pos_3 = (0, 0)                          # this is the position of the :tada: emoji when you win a fight and 2
                                                # of your pokemon's levels up. WARNING : this pixel MUST be a red one
    tagged_strip1 = (0, 0)                      # these are the two coordinates of the yellow strip that stands next to
                                                # a message in which you are pinged. They should look like
    tagged_strip2 = (0, 0)                      # (x, y), (x+1, y), as before.
    background_pos = (0, 0)                     # this should be the position of a pixel that is dark-gray in the first
                                                # message that shows up when you start a fight : this message says you
                                                # challenged X or Y... and waits for 5 seconds before starting the fight
                                                # THIS PIXEL MUST BE A PIXEL THAT WILL BE OF ANOTHER COLOR DURING THE
                                                # FIGHT : usually, it is the coordinate of a dark-gray pixel on the info
                                                # message, but this pixels becomes a green (grass) pixel or something
                                                # when a message showing the state of the fight pops up
    captcha_pos = (0, 0)                        # this is the position of a pixel that is gray-blue, right where the
                                                # bot wrote '#captcha-help' FOR THE FIRST TIME.
                                                # THIS PIXEL MUST BE A GRAY-BLUE ONE


# [---------------------------------------]
# [ DO NOT TOUCH ANYTHING AFTER THIS LINE ]
# [---------------------------------------]

# COLORS
yellow_bar = (255, 166, 0)
tagged = (250, 168, 26)
default_background = (47, 49, 54)
captcha = (75, 68, 59)


def focusLeftWindow():
    pg.keyDown("win")
    pg.press("left")
    pg.keyUp("win")


def focusRightWindow():
    pg.keyDown("win")
    pg.press("right")
    pg.keyUp("win")


def startFight():
    pg.write("mb user 675725560470831125")
    pg.press("enter")


def killFirstPokemon():
    pg.write(secondary_pokemon_attack)
    pg.press("enter")


def switch():
    pg.write("szitch 2")
    pg.press("enter")


def gotTagged(sc):
    return sc.getpixel(tagged_strip1) == tagged or sc.getpixel(tagged_strip1) == tagged


def lookForYellowBand():
    looking = True
    while looking:
        t.sleep(0.1)
        sc = pg.screenshot()
        if sc.getpixel(yellow_bar_pos[0]) == yellow_bar or sc.getpixel(yellow_bar_pos[1]) == yellow_bar or sc.getpixel(yellow_bar_pos[2]) == yellow_bar:
            looking = False
    t.sleep(0.25)


def lookForFightStarted():
    looking = True
    while looking:
        t.sleep(0.1)
        sc = pg.screenshot()
        if sc.getpixel(background_pos) != default_background:
            looking = False
    t.sleep(0.25)


def won(sc):
    return sc.getpixel(end_pos_1)[0] > 150 or sc.getpixel(end_pos_2)[0] > 150 or sc.getpixel(end_pos_3)[0] > 150


def cycle():
    global fighting
    lookForYellowBand()
    sc = pg.screenshot()
    if won(sc):
        fighting = False
    else:
        pg.write(main_pokemon_attack)
        pg.press("enter")


os.system("clear")

focusLeftWindow()


while True:
    startFight()
    t.sleep(2)
    sc = pg.screenshot()
    while sc.getpixel(yellow_bar_pos[0]) != yellow_bar or sc.getpixel(yellow_bar_pos[1]) != yellow_bar or sc.getpixel(yellow_bar_pos[2]) != yellow_bar:
        print("no yellow bar")
        t.sleep(3)
        startFight()
        t.sleep(1)
        sc = pg.screenshot()
        if sc.getpixel(captcha_pos) == captcha:
            print("captcha !")
            exit()
    t.sleep(0.25)

    t.sleep(6)
    killFirstPokemon()
    lookForYellowBand()
    switch()

    fighting = True

    while fighting:
        cycle()

    t.sleep(15)