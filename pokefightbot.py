import os

import pyautogui as pg
import time as t

main_pokemon_attack = "fire punch"
secondary_pokemon_attack = "brutql szing"

red_threshold = 150
green_threshold = 80
yellow_bar = (255, 166, 0)
tagged = (250, 168, 26)
default_background = (47, 49, 54)
captcha = (75, 68, 59)

healthbar_pos = (582, 902)
yellow_bar_pos = [(356, 980), (357, 980), (358, 980)]
end_pos_1 = (529, 478)
end_pos_2 = (529, 458)
end_pos_3 = (529, 438)
tagged_strip1, tagged_strip2 = (291, 960), (292, 960)
background_pos = (652, 933)
captcha_pos = (1045, 912)


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
    tm = t.time()
    while looking:
        if (t.time() - tm)*1000 % 100 == 0:
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
    t.sleep(1)
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
