from PIL import Image, ImageDraw
import numpy as np
import cv2
import time
from mss import mss
import pyautogui
from screeninfo import get_monitors
import subprocess

def test_basic_capture():
    (mon_width, mon_height) = [(m.width, m.height) for m in get_monitors()][0]
    mon = {'left': 0, 'top': 0, 'width': mon_width, 'height': mon_height}

    video = cv2.VideoWriter("output.mp4", 0, 1, (mon_width,mon_height))
    with mss() as sct:
        for i in range(30):
            screenShot = sct.grab(mon)
            img = Image.frombytes(
                'RGB', 
                (screenShot.width, screenShot.height), 
                screenShot.rgb, 
            )
            mpos = pyautogui.position()
            draw = ImageDraw.Draw(img)
            draw.ellipse((mpos.x, mpos.y, mpos.x + 10, mpos.y + 10), fill=(255, 0, 0))

            opencvImage = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

            # img.save(f'output/test{i}.png')
            video.write(opencvImage)
            time.sleep(0.1)
            # one frame is ~600kb
            # 60 frames is ~36mb
            # in reality this was 43mbs (for only 1min)
    video.release()
    subprocess.call(['ffmpeg', '-i', 'output.mp4', '-vcodec', 'libx265', '-crf', '28', 'output_compressed.mp4'])
    # video is 35mb, which is also a lot...
    # and compressed is 500kb. This is kind of ok...
    # ffmpeg -i output.mp4 -vcodec libx265 -crf 28 output_compressed.mp4

    # 1min is 500kb. 1h is 30mb. 24h is 720mb. <- this is a lot, but not terrible.
    # but ok, I should be able to store 1 month worth of data in like 10gb or something.