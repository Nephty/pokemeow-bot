import pyautogui as pg
import sys
import time as t
import os

# COLORS
common = (8, 85, 251)
uncommon = (19, 181, 231)
rare = (251, 138, 8)
superrare = (248, 244, 7)
legendary = (160, 7, 248)
tagged = (250, 168, 26)

# POSIIONS
# edit your coordinates here, you can find them using pyautogui in a console :
# type 'python' in a console then type 'import pyautogui' and 'pyautogui.mouseInfo()'
# read the coordinates from the opened window

# this is the vertical strip indicating the rarity of the pokemon
# it is usually three pixels in width, so enter three different pixel that lay one next to another
strip1, strip2, strip3 = (356, 920), (357, 920), (358, 920)
# that is the bright yellow strip that stands on the very left side of a message in which you're tagged
tagged_strip1, tagged_strip2 = (291, 920), (292, 920)
# that is the position of the pokeball, where you would click to throw a pokeball (the regular one)
pokeball = (320, 980)
# that is the amount of pixels between two balls (how many pixels you have to move right in order to be on
# the next ball, for example : how many pixels do you have to move right from the pokeball in order to be
# on the super ball ?)
spacing_between_pokeballs = 65

# PATH
path = "/home/Nephty/Python/Scripts"

# OTHER VARS
sleeptime = 3
previous_total_executions = 0
total_executions = 0
caught = {
    "common": 0,
    "uncommon": 0,
    "rare": 0,
    "super rare": 0,
    "legendary": 0
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


def gotTagged(sc):
    return sc.getpixel(tagged_strip1) == tagged or sc.getpixel(tagged_strip1) == tagged


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


def cycle():
    global total_executions, sc

    # ADD 1 EXECUTION
    total_executions += 1

    # GENERATE POKEMON
    summonPokemon()

    # IDENTIFY CAPTCHA
    t.sleep(1)

    sc = pg.screenshot()

    if gotTagged(sc):
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
        t.sleep(1)
        sc = pg.screenshot()
        # exit()

    # IDENTIFY RARITY

    strip1_color = sc.getpixel(strip1)
    strip2_color = sc.getpixel(strip2)
    strip3_color = sc.getpixel(strip3)

    pokeball_index = 1

    if isCommon(strip1_color, strip2_color, strip3_color):
        pokeball_index = 1
        caught["common"] += 1

    elif isUncommon(strip1_color, strip2_color, strip3_color):
        pokeball_index = 1
        caught["uncommon"] += 1

    elif isRare(strip1_color, strip2_color, strip3_color):
        pokeball_index = 2
        caught["rare"] += 1

    elif isSuperrare(strip1_color, strip2_color, strip3_color):
        pokeball_index = 3
        caught["super rare"] += 1

    elif isLegendary(strip1_color, strip2_color, strip3_color):
        pokeball_index = 5
        caught["legendary"] += 1

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
    t.sleep(2)
    if pokeball_index == 1:
        pg.write("ms buy 1 1")
        pg.press("enter")
    elif pokeball_index == 2:
        pg.write("ms buy 2 1")
        pg.press("enter")
    elif pokeball_index == 3:
        pg.write("ms buy 3 1")
        pg.press("enter")
    elif pokeball_index == 5:
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
    print(f"running, interval : 11 seconds")
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
