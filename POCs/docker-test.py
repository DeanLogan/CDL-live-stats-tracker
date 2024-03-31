import io
import time
import queue
import sqlite3
import keyboard
import threading
import subprocess
import numpy as np
import pytesseract
from fuzzywuzzy import fuzz
from selenium import webdriver
from PIL import ImageGrab, Image
from difflib import SequenceMatcher
from expiringdict import ExpiringDict
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains

killfeed = ExpiringDict(max_len=9, max_age_seconds=5.5)

kills = {}

deaths = {}

CLAN_TAGS = {
    "toronto ultra": "itori",
    "seattle surge": "iseai",
    "los angeles thieves": "ilati",
    "atlanta faze": "iatli",
    "optic texas": "itxi",
    "new york subliners": "inyi",
    "vegas legion": "ilvi",
    "carolina royal ravens": "icari",
    "los angeles guerrillas": "ilagi",
    "boston breach": "ibosi",
    "miami heretics": "imiai",
    "minnesota rokkr": "imini",
}

def get_players(reader, team1_tag, team2_tag):
    conn = sqlite3.connect('cdl-database.db')
    db = conn.cursor()
    db.execute("SELECT handle FROM Player")
    players = [name[0].lower() for name in db.fetchall()]
    conn.close()

    team1_players = get_text(reader, (203, 310, 537, 326)) # TODO update these values
    team2_players = get_text(reader, (940, 310, 1274, 326)) # TODO update these values

    add_players_to_dicts(team1_players, players, team1_tag)
    add_players_to_dicts(team2_players, players, team2_tag)

def add_players_to_dicts(team_players, players, tag):
    for player in team_players:
        player_name = similar(players, player[1])
        if player_name != "?":
            player_name = (tag + player_name).lower()
            kills[player_name] = 0
            deaths[player_name] = 0

def get_teams(driver):
    conn = sqlite3.connect('cdl-database.db')
    db = conn.cursor()
    db.execute("SELECT name FROM Team")
    team_names = [name[0].lower() for name in db.fetchall()]
    conn.close()
    while True:
        try:
            team1 = similar(team_names, get_text(driver, (200, 212, 537, 239))[0][1]) # TODO update these values
            team2 = similar(team_names, get_text(driver, (940, 212, 1275, 242))[0][1]) # TODO update these values
        except:
            continue
        if team1 != "?" and team2 != "?":
            break
    return team1, team2

def get_text(driver, bbox):
    screenshot = driver.get_screenshot_as_png()
    image = Image.open(io.BytesIO(screenshot))
    roi = image.crop(bbox)
    frame = np.array(roi)
    result = pytesseract.image_to_string(frame, lang='eng')
    return result

def setup_browser():
    print("opening browser")
    options = Options()
    options.headless = True
    driver = webdriver.Firefox()
    driver.install_addon('uBlock0_1.56.1rc5.firefox.signed.xpi', temporary=True) # adding ublock ad blocker
    url = "https://www.youtube.com/watch?v=FjclYlb8dRY&list=WL&index=64" # add this to test for double kills, wait until video is at 3:03 and compare killfeed "&t=160s"
    driver.get(url)
    print("video loaded")
    time.sleep(3) # waits for the video to load

    # click youtubes cookie agreement
    print("clicking cookie agreement")
    button = driver.find_element(by=By.XPATH, value='/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[2]/yt-button-shape/button')
    button.click()

    time.sleep(5) # wait for agreement to be rejected and then click the play button

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
        players = similar(result)
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