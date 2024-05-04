import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sqlite3


team_names_website = {
    "faze": "Atlanta FaZe",
    "breach": "Boston Breach",
    "ravens": "Carolina Royal Ravens",
    "guerrillas": "Los Angeles Guerrillas",
    "thieves": "Los Angeles Thieves",
    "heretics": "Miami Heretics",
    "rokkr": "Minnesota ROKKR",
    "subliners": "New York Subliners",
    "optic": "OpTic Texas",
    "surge": "Seattle Surge",
    "ultra": "Toronto Ultra",
    "legion": "Vegas Legion",
}

# /html/body/div[2]/div/div/div[3]/div/a[1]/div[2]/div/div[2] - xpath of player tags on website
# class="roster-cardstyles__PlayerTag-sc-6tmgp0-4 fVsAmy" - class of player tags on website
# class="roster-cardstyles__PlayerName-sc-6tmgp0-3" - class of player names on website
def get_offical_roster(team_name):
    driver = webdriver.Firefox()
    driver.get(f"https://{team_name}.callofdutyleague.com/en-us/roster") # each team has a different url for their roster

    elements_of_players_handles = driver.find_elements("class name", 'roster-cardstyles__PlayerTag-sc-6tmgp0-4')
    time.sleep(1) # for some reason this sleep needs to be included or else the player names aren't printed, currently assume that the driver.close() at the end is closing the browser before the driver.find_elements() above is finished
    players_handle = [player.text.lower() for player in elements_of_players_handles]

    elements_of_players_names = driver.find_elements("class name", 'roster-cardstyles__PlayerName-sc-6tmgp0-3')
    time.sleep(1) 
    players_name = [player.text.lower() for player in elements_of_players_names]
    
    driver.close()
    return players_handle, players_name

def update_db_with_offical_roster(team_name):
    conn = sqlite3.connect('cdl-database.db')
    db = conn.cursor()
    db.execute("SELECT handle FROM Player WHERE team_name = ?", (team_names_website[team_name],))
    players = [handle[0].lower() for handle in db.fetchall()]
    website_players, names = get_offical_roster(team_name)
    differences = find_differences_in_roster(players, website_players)
    for player in differences:
        if player[1] == "db":
            db.execute("UPDATE Player SET team_name = 'null' WHERE handle = ?", (player[0],))
        else:
            if db.execute("SELECT * FROM Player WHERE handle = ?", (player[0],)).fetchone() is not None:
                db.execute("UPDATE Player SET team_name = ? WHERE handle = ?", (team_names_website[team_name], player[0]))
            else:
                db.execute("INSERT INTO Player (?, ?, ?, ?, ?, ?, ?, ?)", (player[0], names[player[2]], "United States", 0, 0, 0, 0, team_names_website[team_name]))
    conn.close()

def find_differences_in_roster(in_db_players, website_players):
    set1 = set(in_db_players)
    set2 = set(website_players)
    differences = []

    for item in set1.difference(set2):
        index = in_db_players.index(item)
        differences.append((item, "db", index))

    for item in set2.difference(set1):
        index = website_players.index(item)
        differences.append((item, "website", index))

    return differences

if __name__ == "__main__":
    # get_offical_roster("faze") 
    update_db_with_offical_roster("breach")