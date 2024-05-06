import time
from datetime import datetime
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def is_live_on_yt():
    driver = webdriver.Firefox()
    driver = youtube_vid(driver, "https://www.youtube.com/@callofduty/live")
    video_div = driver.find_element("class name", "html5-main-video")
    time.sleep(3) # wait for video to load
    driver.close()
    if video_div != []:
        return True
    else:
        return False

def youtube_vid(driver, url):
    driver.install_addon('uBlock0_1.56.1rc5.firefox.signed.xpi', temporary=True) # adding ublock ad blocker
    driver.get(url)
    print("clicking cookie agreement")
    while True:
        try:
            button = driver.find_element(by=By.XPATH, value='/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/form[1]/div/div/button/span')
            button.click()
            break
        except NoSuchElementException:
            time.sleep(1)

    time.sleep(5) # wait for agreement to be rejected and then click the play button
    return driver

def check_schedule():
    driver = webdriver.Firefox()
    driver.get("https://callofdutyleague.com/en-us/schedule")
    time.sleep(5) # wait for page to load
    start_time = driver.find_element("class name", "match-cardstyles__Left-sc-1rgscfz-5").text
    time.sleep(1)
    driver.close()
    print(start_time)
    if start_time == "LIVE NOW":
        is_live_on_yt()
    else:
        split_time = start_time.split("\n")
        print(split_time[0].split(", ")[1])
        time_of_match = datetime.strptime(split_time[1], "%I:%M %p")
        date = datetime.strptime(split_time[0].split(", ")[1], "%b %d")

        today = datetime.today()
        date = date.replace(year=today.year) # defaults the date to the current year
        combined_datetime = datetime.combine(date.date(), time_of_match.time())

        print(today, date)

        # If the date is in the past, assume it's for next year
        if date.date() < today.date():
            date = date.replace(year=today.year + 1)

        delay = ((combined_datetime - today).total_seconds()) - 300 # seconds until the match starts (- 5 minutes incase a match starts early, which they sometimes do)

        print(combined_datetime)
        print(delay)

        schedule.every(delay).seconds.do(is_live_on_yt)

        # Keep the script running
        while True:
            schedule.run_pending()
            time.sleep(120)

if __name__ == "__main__":
    #is_live_on_yt()
    check_schedule()