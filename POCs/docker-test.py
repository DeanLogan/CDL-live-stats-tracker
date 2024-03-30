import io
import subprocess
from difflib import SequenceMatcher
from PIL import ImageGrab, Image
import time
import numpy as np
import keyboard
import threading
import queue
import pytesseract
from fuzzywuzzy import fuzz
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# the killfeed will not only shows the players name but also the team within a clan tag that typically looks like this [TOR] Scrap, however, the OCR is not able to read the brackets that well and often confuses them wiht I so for the dictionsaries I have hard coded the names with i instead of the brackers (i in lowercase because within the similar function I set what the OCR reads to all lowercase).

kills = {
    "scrap": 2,
    "cleanx": 6,
    "insight": 2,
    "envoy": 2,
    "huke": 4,
    "abuzah": 2,
    "arcitys": 5,
    "breszy": 5
}

deaths = {
    "scrap": 4,
    "cleanx": 3,
    "insight": 4,
    "envoy": 5,
    "huke": 4,
    "abuzah": 5,
    "arcitys": 0,
    "breszy": 3
}

def setup_browser():
    print("opening browser")
    options = Options()
    options.headless = True
    driver = webdriver.Firefox()
    driver.install_addon('uBlock0_1.56.1rc5.firefox.signed.xpi', temporary=True) # adding ublock ad blocker
    url = "https://www.youtube.com/watch?v=FjclYlb8dRY&list=WL&index=64&t=30s"
    driver.get(url)
    print("video loaded")
    time.sleep(3) # Wait for the video to load

    # click youtubes cookie agreement
    print("clicking cookie agreement")
    button = driver.find_element(by=By.XPATH, value='/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[2]/yt-button-shape/button')
    button.click()

    time.sleep(5) # Wait for agreement to be rejected and then click the play button

    # plays yt video as autoplay is off
    print("playing video")
    button = driver.find_element(by=By.XPATH, value='/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[6]/button')
    button.click()

    actions = ActionChains(driver)
    actions.send_keys('m').perform() # press the m key to mute the video
    actions.send_keys('f').perform() # press the f key to go full screen

    time.sleep(0.5) # Wait for full screen animation

    return driver

def capture_images(q, bbox, driver):
    print("starting capture images")

    while True:
        screenshot = driver.get_screenshot_as_png()
        image = Image.open(io.BytesIO(screenshot))
        roi = image.crop(bbox)
        frame = np.array(roi)
        result = pytesseract.image_to_string(frame, lang='eng')
        if len(result) > 6:
            q.put(result)


def process_images(q):
    prev_kill = ""
    while True:
        result = q.get()
        players = identify_names(result)
        if len(players) > 1:
            current_kill = players[0] + " " + players[1]
            if current_kill != prev_kill:
                kill(current_kill)
                prev_kill = current_kill
                print(current_kill)

# this function isn't great maybe another way of identifying the names would be better
def identify_names(input_string):
    identified_names = []

    words = input_string.lower().split()

    for word in words:
        max_score = 0
        max_name = None
        for name in kills:
            score = fuzz.ratio(word, name)
            if score > 60 and score > max_score:
                max_score = score
                max_name = name
        if max_name is not None:
            identified_names.append(max_name)

    return identified_names[:2]


def kill(current_kill):
    killer = current_kill.split(" ")[0]
    killed = current_kill.split(" ")[1]
    kills[killer] += 1
    deaths[killed] += 1

def similar(b):
    most_similar = "?"
    highest_score = 0
    for player in kills:
        score = SequenceMatcher(None, player, b.lower()).ratio()
        if score > highest_score and score > 0.60:
            highest_score = score
            most_similar = player

    return most_similar

def kd():
    for player in kills:
        print(player + " " + str(kills[player]) + " / " + str(deaths[player]))

def testing_selecting_text():
    # bounding box (x1, y1, x2, y2)
    x1, y1, x2, y2 = 44, 640, 365, 667

    screenshot = driver.get_screenshot_as_png()
    image = Image.open(io.BytesIO(screenshot))
    roi = image.crop((x1, y1, x2, y2))
    frame = np.array(roi)
    roi.show()

    screenshot = driver.get_screenshot_as_png()
    image = Image.open(io.BytesIO(screenshot))
    roi = image.crop((x1, y1, x2, y2))
    frame = np.array(roi)
    roi.show()

    screenshot = driver.get_screenshot_as_png()
    image = Image.open(io.BytesIO(screenshot))
    roi = image.crop((x1, y1, x2, y2))
    frame = np.array(roi)
    roi.show()

    screenshot = driver.get_screenshot_as_png()
    image = Image.open(io.BytesIO(screenshot))
    roi = image.crop((x1, y1, x2, y2))
    frame = np.array(roi)
    roi.show()
    
    result = pytesseract.image_to_string(frame, lang='eng')
    print(result)

if __name__ == "__main__":
    print("starting program")
    q = queue.Queue()

    driver = setup_browser()

    capture_thread_1 = threading.Thread(target=capture_images, args=(q,(44, 640, 365, 667), driver,))
    capture_thread_2 = threading.Thread(target=capture_images, args=(q,(44, 613, 365, 640), driver,))
    process_thread = threading.Thread(target=process_images, args=(q,))

    capture_thread_1.start()
    capture_thread_2.start()
    process_thread.start()

    capture_thread_1.join()
    capture_thread_2.join()
    process_thread.join()