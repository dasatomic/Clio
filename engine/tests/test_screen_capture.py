from PIL import Image, ImageDraw
import numpy as np
import cv2
import time
from mss import mss
import pyautogui
from screeninfo import get_monitors

def test_basic_capture():
    (mon_width, mon_height) = [(m.width, m.height) for m in get_monitors()][0]
    mon = {'left': 0, 'top': 0, 'width': mon_width, 'height': mon_height}

    imgs = []
    with mss() as sct:
        for i in range(60):
            screenShot = sct.grab(mon)
            img = Image.frombytes(
                'RGB', 
                (screenShot.width, screenShot.height), 
                screenShot.rgb, 
            )
            mpos = pyautogui.position()
            draw = ImageDraw.Draw(img)
            draw.ellipse((mpos.x, mpos.y, mpos.x + 10, mpos.y + 10), fill=(255, 0, 0))
            img.save(f'output/test{i}.png')
            time.sleep(1)
            # one frame is ~600kb
            # 60 frames is ~36mb
            # in reality this was 43mbs (for only 1min)