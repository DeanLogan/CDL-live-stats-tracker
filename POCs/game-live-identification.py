import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def is_live():
    driver = webdriver.Firefox()
    driver.install_addon('uBlock0_1.56.1rc5.firefox.signed.xpi', temporary=True) # adding ublock ad blocker
    driver = youtube_vid(driver, "https://www.youtube.com/@callofduty/live")
    if driver.find_elements("class name", 'html5-main-video') != []:
        return True
    else:
        return False

def youtube_vid(driver, url):
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

if __name__ == "__main__":
    is_live()