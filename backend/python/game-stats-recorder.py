import io
import time
import queue
import easyocr
import sqlite3
import threading
import numpy as np
from selenium import webdriver
from PIL import ImageGrab, Image
from difflib import SequenceMatcher
from expiringdict import ExpiringDict
from selenium.webdriver.common.by import By
from confluent_kafka import Producer, KafkaException
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

killfeed = ExpiringDict(max_len=9, max_age_seconds=5.5)

team1, team2 = ""

kills, deaths = {}

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

    team1_players = get_text(reader, (134, 166, 650, 197)) 
    team2_players = get_text(reader, (1266, 168, 1788, 197))

    print(f"====== {team1_players}")
    print(f"====== {team2_players}")

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
    team1, team2 = "?", "?"
    while True:
        try:
            team1 = similar(team_names, get_text(driver, (133, 18, 653, 64))[0][1]) 
            team2 = similar(team_names, get_text(driver, (1266, 17, 1788, 64))[0][1]) 
        except Exception as e:
            continue
        if team1 != "?" and team2 != "?":
            break
    return team1, team2

def setup_browser():
    print("opening browser")
    options = Options()
    options.headless = True
    driver = webdriver.Firefox()
    driver.set_window_size(1920, 1080)
    driver.install_addon('uBlock0_1.56.1rc5.firefox.signed.xpi', temporary=True) # adding ublock ad blocker
    url = "https://www.youtube.com/watch?v=FjclYlb8dRY&list=WL&index=64" # add this "&t=164s" to test for double kills, wait until video is at 3:03 and compare killfeed 
    driver.get(url)
    print("video loaded")
    time.sleep(3) # waits for the video to load

    # click youtubes cookie agreement
    print("clicking cookie agreement")
    while True:
        try:
            button = driver.find_element(by=By.XPATH, value='/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[2]/yt-button-shape/button')
            button.click()
            break
        except NoSuchElementException:
            time.sleep(1)

    time.sleep(5) # wait for agreement to be rejected and then click the play button

    # plays yt video as autoplay is off
    print("playing video")
    while True:
        try:
            button = driver.find_element(by=By.XPATH, value='/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[6]/button')
            button.click()
            break
        except NoSuchElementException:
            time.sleep(1)

    actions = ActionChains(driver)
    actions.send_keys('m').perform() # press the m key to mute the video
    actions.send_keys('f').perform() # press the f key to go full screen

    time.sleep(0.5) # wait for full screen animation

    return driver

def get_text(reader, bbox):
    screenshot = driver.get_screenshot_as_png()
    image = Image.open(io.BytesIO(screenshot))
    roi = image.crop(bbox)
    npArray = np.array(roi)
    result = reader.readtext(npArray)
    return result

def capture_killfeed(q, bbox, driver):
    print("Capture thread started")
    while True:
        screenshot = driver.get_screenshot_as_png()
        image = Image.open(io.BytesIO(screenshot))
        roi = image.crop(bbox)
        result = np.array(roi)
        if len(result) > 1:
            q.put(result)


def process_images(q, reader):
    print("Process thread started")
    players=["itoriscrap", "itoricleanx", "itoriinsight", "itorienvoy", "iseaihuke", "iseaiabuzah", "iseaiarcitys", "iseaibreszy"]
    while True:
        result = q.get()
        estimated_words = reader.readtext(result)
        if len(estimated_words) > 1:
            current_kill = similar(players, estimated_words[0][1]) + " " + similar(players, estimated_words[1][1])
            if (not killfeed.get(current_kill, False)) and current_kill[0] != "?" and current_kill[len(current_kill)-1] != "?":
                killfeed[current_kill] = True
                print(current_kill)
                kill(current_kill)

def test_capture_and_process(bbox, driver, reader):
    players=["itoriscrap", "itoricleanx", "itoriinsight", "itorienvoy", "iseaihuke", "iseaiabuzah", "iseaiarcitys", "iseaibreszy"]
    while True:
        screenshot = driver.get_screenshot_as_png()
        image = Image.open(io.BytesIO(screenshot))
        roi = image.crop(bbox)
        npArray = np.array(roi)
        result = reader.readtext(npArray)
        if len(result) > 1:
            current_kill = similar(players, result[0][1]) + " " + similar(players, result[1][1])
            if (not killfeed.get(current_kill, False)) and current_kill[0] != "?" and current_kill[len(current_kill)-1] != "?":
                killfeed[current_kill] = True
                print(current_kill)
                kill(current_kill)

def kill(current_kill):
    current_kill_split = current_kill.split(" ")
    killer = current_kill_split[0]
    killed = current_kill_split[1]
    kills[killer] += 1
    deaths[killed] += 1
    p.produce('test', {
        "team1":team1,
        "team2":team2,
        "killRecord":kills, 
        "deathRecord":deaths,
        })
    p.flush()

def similar(similar_words, str):
    most_similar = "?"
    highest_score = 0
    str  = str.lower()
    for word in similar_words:
        score = SequenceMatcher(None, word, str).ratio()
        if score > highest_score and score > 0.60:
            highest_score = score
            most_similar = word

    return most_similar

def kd():
    for player in kills:
        print(player + " " + str(kills[player]) + " / " + str(deaths[player]))

if __name__ == "__main__":
    # start the kafka producer server
    while True:
        bootstrap_servers = 'kafka:9092' 
        print(f'Connecting to {bootstrap_servers}')

        p = Producer({'bootstrap.servers': bootstrap_servers})

        try:
            # Try to flush the messages. If it returns 0, break the loop.
            if p.flush(timeout=10.0) == 0:
                print('Connected successfully.')
                break
        except KafkaException as e:
            print(f'Failed to connect: {e}')
            time.sleep(5)
            continue

    # start selenium to "watch" the match
    print("starting selenium and easyocr script")
    reader = easyocr.Reader(['en'])
    q = queue.Queue()

    driver = setup_browser()

    print("browser setup, trying to get team names")

    team1, team2 = get_teams(reader)

    print(team1, team2)

    get_players(reader, CLAN_TAGS[team1], CLAN_TAGS[team2])

    for player in kills:
        print(player)

    bboxes = [(44, 637, 365, 667),(44, 610, 365, 640),(44, 637, 365, 667),(44, 610, 365, 640)]

    for bbox in bboxes:
        thread = threading.Thread(target=capture_killfeed, args=(q, bbox, driver))
        thread.start()

    for i in range(0, len(bboxes)):
        thread = threading.Thread(target=process_images, args=(q, reader))
        thread.start()