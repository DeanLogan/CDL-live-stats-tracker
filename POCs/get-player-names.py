from difflib import SequenceMatcher
import sqlite3
import easyocr

from PIL import ImageGrab
import numpy as np

kills = {}

deaths = {}

CLAN_TAGS = {
    "Toronto Ultra": "itori",
    "Seattle Surge": "iseai",
    "Los Angeles Thieves": "ilati",
    "Atlanta FaZe": "iatli",
    "OpTic Texas": "itxi",
    "New York Subliners": "inyi",
    "Vegas Legion": "ilvi",
    "Carolina Royal Ravens": "icari",
    "Los Angeles Guerrillas": "ilagi",
    "Boston Breach": "ibosi",
    "Miami Heretics": "imiai",
    "Minnesota ROKKR": "imini",
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
    print(players)
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
    team1 = similar(team_names, get_text(reader, (200, 212, 537, 239))[0][1])
    team2 = similar(team_names, get_text(reader, (940, 212, 1275, 242))[0][1])
    if team1 in team_names and team2 in team_names:
        print(team1 + " vs " + team2)

def get_text(reader, bbox):
    img = ImageGrab.grab(bbox=bbox)
    npArray = np.array(img)
    result = reader.readtext(npArray)
    return result

if __name__ == "__main__":
    reader = easyocr.Reader(['en'])
    get_teams(reader)
    get_players(reader, CLAN_TAGS["seattle surge"], CLAN_TAGS["toronto ultra"])