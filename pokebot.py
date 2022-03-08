import pyautogui as pg
import sys
import time as t
import os

# COORDINATES & PATH (only edit the 'else' segment)
if os.environ['HOSTNAME'] == 'fedora':
    # don't edit anything here it's useless
    strip1 = (2954, 1270)
    strip2 = (2955, 1270)
    strip3 = (2956, 1270)
    tagged_strip1_upper = (2882, 1285)
    tagged_strip2_upper = (2883, 1285)
    tagged_strip1_lower = (2882, 1335)
    tagged_strip2_lower = (2883, 1335)
    pokeball = (2986, 1326)
    spacing_between_pokeballs = 72
    path = "/home/Nephty/Python/Projects/pokemeow-bot"
elif os.environ['HOSTNAME'] == 'nephty-fedora':
    # don't edit anything here it's useless
    strip1 = (356, 920)
    strip2 = (357, 920)
    strip3 = (358, 920)
    tagged_strip1_upper = (291, 920)
    tagged_strip2_upper = (292, 920)
    tagged_strip1_lower = (291, 970)
    tagged_strip2_lower = (292, 970)
    pokeball = (385, 980)
    spacing_between_pokeballs = 65
    path = "/home/Nephty/Python/Projects/pokemeow-bot"
else:
    # CHANGE THESE VARIABLES so that they match the coordinates on your screen (x, y)
    # Read the README.md if you don't know how to get the coordinates of a pixel on your screen
    strip1 = (0, 0)                 # these are the three coordinates of the blue/orange/purple... strip that stands
    strip2 = (0, 0)                 # next to a message coming from the bot when you run ;p. These coordinates should be
    strip3 = (0, 0)                 # looking like : (x, y), (x+1, y), (x+2, y) where x and y are your custom coos.
    tagged_strip1_upper = (0, 0)    # these are the two coordinates of the yellow strip that stands next to a message
    tagged_strip2_upper = (0, 0)    # in which you are pinged. They should look like (x, y), (x+1, y), as before.
                                    # they should be the upper part of the strip, when the bot tags you for a catpcha
    tagged_strip1_lower = (tagged_strip1_upper[0], tagged_strip1_upper[1]+50)
    tagged_strip2_lower = (tagged_strip2_upper[0], tagged_strip2_upper[1]+50)
    pokeball = (0, 0)               # this is the coordinate of the pokeball that shows up below a pokemon you can catch
    spacing_between_pokeballs = 0   # this is the spacing between the pokeball and the superball (measured in pixels)
    path = ""                       # this is the path of the directory in which this exact python file is located


# [---------------------------------------]
# [ DO NOT TOUCH ANYTHING AFTER THIS LINE ]
# [---------------------------------------]

# COLORS
common = (8, 85, 251)
uncommon = (19, 181, 231)
rare = (251, 138, 8)
superrare = (248, 244, 7)
legendary = (160, 7, 248)
shiny = (255, 153, 204)
tagged = (250, 168, 26)

# OTHER VARS
sleeptime = 3
previous_total_executions = 0
total_executions = 0
caught = {
    "common": 0,
    "uncommon": 0,
    "rare": 0,
    "super rare": 0,
    "legendary": 0,
    "shiny": 0
}
sc = None

with open(f"{path}/pokebot_total", "r") as f:
    total_executions = int(f.readline())
    previous_total_executions = total_executions


def focusLeftWindow():
    pg.keyDown("win")
    pg.press("left")
    pg.keyUp("win")


def focusRightWindow():
    pg.keyDown("win")
    pg.press("right")
    pg.keyUp("win")


def summonPokemon():
    pg.press("space")
    pg.write("mp")
    pg.press("enter")


def gotTaggedUpper(sc):
    return sc.getpixel(tagged_strip1_upper) == tagged or sc.getpixel(tagged_strip1_upper) == tagged


def gotTaggedLower(sc):
    return sc.getpixel(tagged_strip1_lower) == tagged or sc.getpixel(tagged_strip1_lower) == tagged


def printSession():
    print("[====================]")
    print("| Session results :  |")
    for key in caught.keys():
        print(f"|   {key[0].upper()}{key[1:]}s : {caught[key]}{(10 - (len(key) + len(str(caught[key])) - 3)) * ' '}|")
    print("[====================]")
    print("| Total executions : |")
    print(f"|   {total_executions}{(17 - (len(str(total_executions))))*' '}|")
    print("| In this session :  |")
    print(f"|   {total_executions - previous_total_executions}{(17 - (len(str(total_executions - previous_total_executions))))*' '}|")
    print("[====================]")


def isCommon(p1, p2, p3):
    return p1 == common or p2 == common or p3 == common


def isUncommon(p1, p2, p3):
    return p1 == uncommon or p2 == uncommon or p3 == uncommon


def isRare(p1, p2, p3):
    return p1 == rare or p2 == rare or p3 == rare


def isSuperrare(p1, p2, p3):
    return p1 == superrare or p2 == superrare or p3 == superrare


def isLegendary(p1, p2, p3):
    return p1 == legendary or p2 == legendary or p3 == legendary


def isShiny(p1, p2, p3):
    return p1 == shiny or p2 == shiny or p3 == shiny


def cycle():
    global total_executions, sc

    # ADD 1 EXECUTION
    total_executions += 1

    # GENERATE POKEMON
    summonPokemon()

    # IDENTIFY CAPTCHA
    t.sleep(2)

    sc = pg.screenshot()

    if gotTaggedUpper(sc) and gotTaggedLower(sc):
        os.system("clear")
        printSession()
        print(f"Captcha !")
        focusRightWindow()
        captcha_code = input("Enter captcha code >> ")
        focusLeftWindow()
        pg.write(captcha_code)
        pg.press("enter")
        t.sleep(1)
        summonPokemon()
        t.sleep(1.5)
        sc = pg.screenshot()
    elif gotTaggedLower(sc):
        t.sleep(3)
        summonPokemon()
        t.sleep(1.5)
        sc = pg.screenshot()

    # IDENTIFY RARITY

    strip1_color = sc.getpixel(strip1)
    strip2_color = sc.getpixel(strip2)
    strip3_color = sc.getpixel(strip3)

    pokeball_index = 0

    if isCommon(strip1_color, strip2_color, strip3_color):
        pokeball_index = 0
        caught["common"] += 1

    elif isUncommon(strip1_color, strip2_color, strip3_color):
        pokeball_index = 0
        caught["uncommon"] += 1

    elif isRare(strip1_color, strip2_color, strip3_color):
        pokeball_index = 1
        caught["rare"] += 1

    elif isSuperrare(strip1_color, strip2_color, strip3_color):
        pokeball_index = 2
        caught["super rare"] += 1

    elif isLegendary(strip1_color, strip2_color, strip3_color):
        pokeball_index = 4
        caught["legendary"] += 1

    elif isShiny(strip1_color, strip2_color, strip3_color):
        pokeball_index = 2
        caught["shiny"] += 1

    else:
        os.system("clear")
        print("Unknown color.")
        printSession()
        focusRightWindow()
        exit()

    # CATCH IT
    pg.moveTo(pokeball[0] + pokeball_index * spacing_between_pokeballs, pokeball[1])
    pg.click()

    # BUY POKEBALLS
    t.sleep(1.5)
    if pokeball_index == 0:
        pg.write("ms buy 1 1")
        pg.press("enter")
    elif pokeball_index == 1:
        pg.write("ms buy 2 1")
        pg.press("enter")
    elif pokeball_index == 2:
        pg.write("ms buy 3 1")
        pg.press("enter")
    elif pokeball_index == 4:
        pg.write("ms buy 4 1")

    # RELEASE DUPLICATES
    t.sleep(2.5)
    pg.write("mr d")
    pg.press("enter")

    # OPEN LOOTBOXES
    t.sleep(2.5)
    pg.write("mlootbox qll")
    pg.press("enter")


def run(st=sleeptime, times=-1):
    if times < 0:
        while True:
            cycle()
            t.sleep(st)
    else:
        for i in range(times):
            print(f"times left : {times - i}")
            cycle()
            t.sleep(st)
        print(f"done !")
        print(f"ran {times} times")


try:
    os.system("clear")
    print(f"running, interval : 12 seconds")
    if len(sys.argv) == 1:
        t.sleep(1)
        focusLeftWindow()
        run()
    elif len(sys.argv) == 2:
        t.sleep(1)
        focusLeftWindow()
        pg.write(sys.argv[1])
        pg.press("enter")
        t.sleep(1)
        run()
    else:
        print("Invalid amount of arguments.")
        exit()

except KeyboardInterrupt:
    print()
    printSession()

with open(f"{path}/pokebot_total", "w") as f:
    f.truncate()
    f.write(str(total_executions))
