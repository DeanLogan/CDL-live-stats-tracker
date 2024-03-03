import easyocr

from PIL import ImageGrab, Image
import pyautogui
import time
import pytesseract
import numpy as np
import time

def test_from_png():
    # Create a reader for English
    reader = easyocr.Reader(['en'])

    # Perform OCR on an image
    result = reader.readtext('./imgs/killfeed.png')

    # Print the result
    for detection in result:
        text = detection[1]
        print(text)

    print("=====================================")

    print(result)

    # # Perform OCR on an image
    # result = reader.readtext('./imgs/player-faces.png')

    # # Print the result
    # for detection in result:
    #     text = detection[1]
    #     print(text)


def test_from_screen():
    reader = easyocr.Reader(['en'])
    prev_result = []
    while True:
        img = ImageGrab.grab(bbox=(131, 610, 339, 627))
        npArray = np.array(img)
        result = reader.readtext(npArray)
        if len(result) > 1:
            
            print(result[0][1], result[1][1])
            prev_result = result
        time.sleep(0.1)

if __name__ == "__main__":
    # test_from_png()
    test_from_screen()