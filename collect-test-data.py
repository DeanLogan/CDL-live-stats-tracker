from difflib import SequenceMatcher
import easyocr

from PIL import ImageGrab
import time
import numpy as np
import time
import keyboard

import threading
import queue

sea = ["iseaihuke", "iseaiabuzah", "iseaiarcitys", "iseaibreszy"]
tor = ["itoriscrap", "itoricleanx", "itoriinsight", "itorienvoy"]
min = ["iminilyynz", "iminiaccuracy", "iminiowakening", "iminivivid"]
lat = ["ilatighosty", "ilatikremp", "ilatinastie", "ilatiafro"]


def capture_images(results, images):
    reader = easyocr.Reader(['en'])
    while True:
        img = ImageGrab.grab(bbox=(131, 610, 339, 638))
        npArray = np.array(img)
        result = reader.readtext(npArray)
        if len(result) > 1:
            results.put(result)
            images.put(img)

def process_images(results, images):
    players=["itoriscrap", "itoricleanx", "itoriinsight", "itorienvoy", "iseaihuke", "iseaiabuzah", "iseaiarcitys", "iseaibreszy"]
    prev_kill = ""
    while True:
        result = results.get()
        current_kill = similar(players, result[0][1]) + " " + similar(players, result[1][1])
        if current_kill != prev_kill and current_kill[0] != "?" and current_kill[len(current_kill)-1] != "?":
            img = images.get()
            prev_kill = current_kill
            img.save(f"training-data/{current_kill}.png")
            print(current_kill)

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
    results = queue.Queue()
    images = queue.Queue()
    capture_thread = threading.Thread(target=capture_images, args=(results, images,))
    process_thread = threading.Thread(target=process_images, args=(results, images,))
    capture_thread.start()
    process_thread.start()