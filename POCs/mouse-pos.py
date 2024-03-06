import pyautogui
import time

def mouse_pos():
    last_position = pyautogui.position()

    while True:
        current_position = pyautogui.position()
        if current_position != last_position:
            print(current_position)
            last_position = current_position
        time.sleep(0.001)  # pause for 100 milliseconds

if __name__ == "__main__":
    mouse_pos()