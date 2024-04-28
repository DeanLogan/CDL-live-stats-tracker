import io
from PIL import Image, ImageGrab

def screenshot(bbox):
    screenshot = ImageGrab.grab(bbox=bbox)
    screenshot.show()

if __name__ == "__main__":
    screenshot((134, 166, 650, 197))
    screenshot((1266, 168, 1788, 197))
    screenshot((133, 18, 653, 64))
    screenshot((1266, 17, 1788, 64))