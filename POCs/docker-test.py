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
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def stream_youtube_video():
    video_url = "https://www.youtube.com/watch?v=FjclYlb8dRY&list=WL&index=61&t=127s"
    ffmpeg_command = f"youtube-dl -q -o - {video_url} | ffmpeg -i pipe:0 -f mp4 -vcodec rawvideo -"

    process = subprocess.Popen(ffmpeg_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    
    process.stdout.close()
    process.stderr.close()


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


def capture_images(q):
    print("capturing images starting")

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    url = "https://www.youtube.com/watch?v=FjclYlb8dRY&list=WL&index=61&t=127s"
    driver.get(url)
    print("video loaded")
    # Wait for the video to load
    time.sleep(5)

    # bounding box (x1, y1, x2, y2)
    x1, y1, x2, y2 = 144, 616, 350, 635

    while True:
        screenshot = driver.get_screenshot_as_png()
        image = Image.open(io.BytesIO(screenshot))
        roi = image.crop((x1, y1, x2, y2))
        frame = np.array(roi)
        result = pytesseract.image_to_string(frame, lang='eng')
        print(result)
        if len(result) > 6:
            q.put(result)
        time.sleep(0.1)


def process_images(q):
    players=["itoriscrap", "itoricleanx", "itoriinsight", "itorienvoy", "iseaihuke", "iseaiabuzah", "iseaiarcitys", "iseaibreszy"]
    prev_kill = ""
    while True:
        result = q.get()
        print(result)
        players = identify_names(result)
        if len(players) > 1:
            current_kill = players[0] + " " + players[1]
            if current_kill != prev_kill:
                print("------------------------------------")
                kill(current_kill)
                print("====================================")
                prev_kill = current_kill
                print(current_kill)
                kd()
                print("------------------------------------")

# this function isn't great maybe another way of identifying the names would be better
def identify_names(input_string):
    identified_names = []
    scores = []

    words = input_string.lower().split()

    for word in words:
        max_score = 0
        max_name = None
        for name in kills:
            score = fuzz.ratio(word, name)
            if score > 55 and score > max_score:
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

if __name__ == "__main__":
    print("starting program")
    stream_youtube_video()
    q = queue.Queue()
    capture_thread = threading.Thread(target=capture_images, args=(q,))
    process_thread = threading.Thread(target=process_images, args=(q,))
    capture_thread.start()
    process_thread.start()

    capture_thread.join()
    process_thread.join()