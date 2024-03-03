from difflib import SequenceMatcher
import easyocr

from PIL import ImageGrab
import time
import numpy as np
import time
import keyboard

# the killfeed will not only shows the players name but also the team within a clan tag that typically looks like this [TOR] Scrap, however, the OCR is not able to read the brackets that well and often confuses them wiht I so for the dictionsaries I have hard coded the names with i instead of the brackers (i in lowercase because within the similar function I set what the OCR reads to all lowercase).

# kills = {
#     "itoriscrap: 0,
#     "itoricleanx": 2,
#     "itoriinsight": 2,
#     "itorienvoy": 1,
#     "iseaihuke": 4,
#     "iseaiabuzah": 1,
#     "iseaiarcityss": 3,
#     "iseaibreszy": 2
# }

# deaths = {
#     "itoriscrap": 3,
#     "itoricleanx": 2,
#     "itoriinsight": 2,
#     "itorienvoy": 3,
#     "iseaihuke": 2,
#     "iseaiabuzah": 2,
#     "iseaiarcitys": 0,
#     "iseaibreszy": 1
# }

kills = {
    "itoriscrap": 2,
    "itoricleanx": 6,
    "itoriinsight": 2,
    "itorienvoy": 2,
    "iseaihuke": 4,
    "iseaiabuzah": 2,
    "iseaiarcitys": 5,
    "iseaibreszy": 5
}

deaths = {
    "itoriscrap": 4,
    "itoricleanx": 3,
    "itoriinsight": 4,
    "itorienvoy": 5,
    "iseaihuke": 4,
    "iseaiabuzah": 5,
    "iseaiarcitys": 0,
    "iseaibreszy": 3
}

# TODO - currently 
def read_killfeed():
    players=["itoriscrap", "itoricleanx", "itoriinsight", "itorienvoy", "iseaihuke", "iseaiabuzah", "iseaiarcitys", "iseaibreszy"]
    reader = easyocr.Reader(['en'])
    prev_kill = ""
    while True:
        if keyboard.is_pressed('esc'):
            print('You Pressed A Key!')
            kd()
            break  # finish the loop
        img = ImageGrab.grab(bbox=(131, 610, 339, 627)) # currently takes a section of my screen on where the killfeed is located, however the plan is to eventually change this to programatically find the killfeed on the screen
        npArray = np.array(img)
        result = reader.readtext(npArray)
        if len(result) > 1:
            current_kill = similar(players, result[0][1]) + " " + similar(players, result[1][1])
            if current_kill != prev_kill and current_kill[0] != "?" and current_kill[len(current_kill)-1] != "?":
                prev_kill = current_kill
                kill(current_kill)

def kd():
    for player in kills:
        print(player + " " + str(kills[player]) + " / " + str(deaths[player]))

def kill(current_kill):
    killer = current_kill.split(" ")[0]
    killed = current_kill.split(" ")[1]
    kills[killer] += 1
    deaths[killed] += 1


def similar(players, b):
    most_similar = "?"
    highest_score = 0
    for player in players:
        score = SequenceMatcher(None, player, b.lower()).ratio()
        if score > highest_score and score > 0.60:
            highest_score = score
            most_similar = player

    return most_similar

if __name__ == "__main__":
    read_killfeed()
    # players=["scrap", "cleanx", "insight", "envoy", "huke", "abuzah", "arcitys"]
    # print(similar(players, "ITORI Clean"))