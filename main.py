from expiringdict import ExpiringDict
from difflib import SequenceMatcher
from PIL import ImageGrab
import numpy as np
import threading
import keyboard
import sqlite3
import easyocr
import queue
import sys


killfeed = ExpiringDict(max_len=9, max_age_seconds=5)

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

def similar(similar_words, str):
    most_similar = "?"
    highest_score = 0
    for word in similar_words:
        score = SequenceMatcher(None, word, str.lower()).ratio()
        if score > highest_score and score > 0.60:
            highest_score = score
            most_similar = word

    return most_similar

def get_players(reader, team1_tag, team2_tag):
    conn = sqlite3.connect('cdl-database.db')
    db = conn.cursor()
    db.execute("SELECT handle FROM Player")
    players = [name[0].lower() for name in db.fetchall()]
    conn.close()

    team1_players = get_text(reader, (203, 310, 537, 326))
    team2_players = get_text(reader, (940, 310, 1274, 326))

    add_players_to_dicts(team1_players, players, team1_tag)
    add_players_to_dicts(team2_players, players, team2_tag)

def add_players_to_dicts(team_players, players, tag):
    for player in team_players:
        player_name = similar(players, player[1])
        if player_name != "?":
            player_name = (tag + player_name).lower()
            kills[player_name] = 0
            deaths[player_name] = 0

def get_teams(reader):
    conn = sqlite3.connect('cdl-database.db')
    db = conn.cursor()
    db.execute("SELECT name FROM Team")
    team_names = [name[0].lower() for name in db.fetchall()]
    conn.close()
    while True:
        try:
            team1 = similar(team_names, get_text(reader, (200, 212, 537, 239))[0][1])
            team2 = similar(team_names, get_text(reader, (940, 212, 1275, 242))[0][1])
        except:
            continue
        if team1 != "?" and team2 != "?":
            break
    return team1, team2

def get_text(reader, bbox):
    img = ImageGrab.grab(bbox=bbox)
    npArray = np.array(img)
    result = reader.readtext(npArray)
    return result

def capture_killfeed(q, reader, bbox):
    print("Capture thread started")
    while True:
        img = ImageGrab.grab(bbox=bbox)
        npArray = np.array(img)
        result = reader.readtext(npArray)
        if len(result) > 1:
            q.put(result)

def process_images(q):
    print("Process thread started")
    while True:
        result = q.get()
        if len(result) > 1:
            current_kill = similar(kills, result[0][1]) + " " + similar(kills, result[1][1])
            if (not killfeed.get(current_kill, False)) and current_kill[0] != "?" and current_kill[len(current_kill)-1] != "?":
                killfeed[current_kill] = True
                print(current_kill)
                kill(current_kill)

def kill(current_kill):
    killer = current_kill.split(" ")[0]
    killed = current_kill.split(" ")[1]
    kills[killer] += 1
    deaths[killed] += 1

def kd():
    for player in kills:
        print(player + " " + str(kills[player]) + " / " + str(deaths[player]))

if __name__ == "__main__":
    reader = easyocr.Reader(['en'])
    team1, team2 = get_teams(reader)
    get_players(reader, CLAN_TAGS[team1], CLAN_TAGS[team2])

    print(kills)

    q = queue.Queue()
    
    capture_thread_1 = threading.Thread(target=capture_killfeed, args=(q,reader, (144, 616, 350, 635),), daemon=True)
    capture_thread_2 = threading.Thread(target=capture_killfeed, args=(q,reader, (144, 595, 350, 615),), daemon=True)
    process_thread = threading.Thread(target=process_images, args=(q,), daemon=True)

    capture_thread_1.start()
    capture_thread_2.start()
    process_thread.start()

    while True:
        if keyboard.is_pressed('esc'):
            kd()
            sys.exit()

