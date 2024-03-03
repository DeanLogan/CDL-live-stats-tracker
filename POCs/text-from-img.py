from PIL import ImageGrab, Image
import pyautogui
import time
import pytesseract
import numpy as np
import cv2

def main():
    lastFeed = ""
    while True:
    # img = Image.open('./imgs/360p-killfeed.png')
        img = ImageGrab.grab(bbox=(131, 610, 339, 627))
        npArray = np.array(img)
        feed = pytesseract.image_to_string(npArray)
        if feed != lastFeed:
            print(feed)
            lastFeed = feed
        if pyautogui.hotkey('esc'):
            break

def mouse_pos():
    last_position = pyautogui.position()

    while True:
        current_position = pyautogui.position()
        if current_position != last_position:
            print(current_position)
            last_position = current_position
        time.sleep(0.001)  # pause for 100 milliseconds

if __name__ == "__main__":
    main()
    # mouse_pos()