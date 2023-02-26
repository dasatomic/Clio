import subprocess
import cv2
import numpy as np
import pyautogui
from screeninfo import get_monitors
from PIL import Image, ImageDraw
from mss import mss
import datetime

class ImageWithTimeStamp:
    def __init__(self, image, timestamp):
        self.image = image
        self.timestamp = timestamp

class ScreenRecorder:
    def __init__(self):
        pass
        # TODO:this works only for the first monitor
        # add multimonitor support
        (self.mon_width, self.mon_height) = [(m.width, m.height) for m in get_monitors()][0]
        self.mon = {'left': 0, 'top': 0, 'width': self.mon_width, 'height': self.mon_height}
        self.image_history = []
        self.sct = mss()
    
    def take_screenshot(self):
        screenShot = self.sct.grab(self.mon)
        img = Image.frombytes(
            'RGB', 
            (screenShot.width, screenShot.height), 
            screenShot.rgb, 
        )

        # draw a red dot at the mouse position
        mpos = pyautogui.position()
        draw = ImageDraw.Draw(img)
        draw.ellipse((mpos.x, mpos.y, mpos.x + 10, mpos.y + 10), fill=(255, 0, 0))

        self.image_history.append(ImageWithTimeStamp(img, datetime.datetime.now()))

    def save_batch(self, batch_name):
        video = cv2.VideoWriter("raw_video.mp4", 0, 1, (self.mon_width,self.mon_height))
        for img in self.image_history:
            opencvImage = cv2.cvtColor(np.array(img.image), cv2.COLOR_RGB2BGR)
            video.write(opencvImage)
        video.release()
        # call ffmpeg to compress the video
        subprocess.call(['ffmpeg', '-i', 'output.mp4', '-vcodec', 'libx265', '-crf', '28', batch_name + '_compressed.mp4'])
        self.image_history.clear()
        # todo: log the size and time taken.

    def extract_batch(self, batch_name):
        # TODO: work in temp directory.
        subprocess.call(['ffmpeg', '-i', batch_name + '_compressed.mp4', '-r', '1/1' 'from_compressed%03d.jpg]'])

    def get_history_len(self):
        self.image_history.len()