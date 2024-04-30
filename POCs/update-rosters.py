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
def get_roster(team_name):
    driver = webdriver.Firefox()
    driver.get(f"https://{team_name}.callofdutyleague.com/en-us/roster") # each team has a different url for their roster

    elements_of_players_handles = driver.find_elements("class name", 'roster-cardstyles__PlayerTag-sc-6tmgp0-4')
    time.sleep(1) # for some reason this sleep needs to be included or else the player names aren't printed, currently assume that the driver.close() at the end is closing the browser before the driver.find_elements() above is finished
    players_handle = [player.text.lower() for player in elements_of_players_handles]

    elements_of_players_names = driver.find_elements("class name", 'roster-cardstyles__PlayerName-sc-6tmgp0-3')
    time.sleep(1) 
    players_name = [player.text.lower() for player in elements_of_players_names]
    
    print("worked?")
    driver.close()

def replace_roster_in_db():
    conn = sqlite3.connect('cdl-database.db')
    db = conn.cursor()
    db.execute("SELECT name FROM Team")
    print(db.fetchall())
    conn.close()

if __name__ == "__main__":
    # get_roster("faze") 
    replace_roster_in_db()