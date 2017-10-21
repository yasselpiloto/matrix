import time
import os
from picamera import PiCamera

def capture_images(save_folder):
    """Stream images off the camera and save them."""
    camera = PiCamera()
    camera.resolution = (320, 240)
    camera.vflip = True
    camera.framerate = 10

    # Warmup...
    time.sleep(2)

    # And capture continuously forever.
    for _ in camera.capture_continuous(save_folder + '{timestamp}.jpg', 'jpeg', use_video_port=True):
        pass

capture_images(os.environ['CAPTURE_PATH'])
