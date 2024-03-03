# imports
from PIL import ImageGrab
from PIL import Image
import numpy as np
import pytesseract
import argparse
import cv2
import os

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1366, 768))

while(True):
        x = 760
        y = 968

        ox = 50
        oy = 22

        # screen capture
        img = ImageGrab.grab(bbox=(x, y, x + ox, y + oy))
        img_np = np.array(img)
        frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        cv2.imshow("Screen", frame)
        # below from stackoverflow - https://stackoverflow.com/questions/14655969/opencv-v1-v2-error-the-function-is-not-implemented
        # img = cv2.imread('path_to_image')
        # plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
        # plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
        # plt.show()
        out.write(frame)

        if cv2.waitKey(1) == 0:
                break

out.release()
cv2.destroyAllWindows()