import time
from selenium import webdriver

def get_roster(team_name):
    driver = webdriver.Firefox()
    driver.get(f"https://{team_name}.callofdutyleague.com/en-us/roster") # each team has a different url for their roster
    players = driver.find_elements("class name", 'roster-cardstyles__PlayerTag-sc-6tmgp0-4')
    time.sleep(1) # for some reason this sleep needs to be included or else the player names aren't printed, currently assume that the driver.close() at the end is closing the browser before the driver.find_elements() above is finished
    for player in players:
        print(player.text.lower())
    print("worked?")
    # /html/body/div[2]/div/div/div[3]/div/a[1]/div[2]/div/div[2] - xpath of player tags on website
    # class="roster-cardstyles__PlayerTag-sc-6tmgp0-4 fVsAmy" - class of player tags on website
    driver.close()

if __name__ == "__main__":
    get_roster("faze") 