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
    #for _ in camera.capture_continuous(save_folder + '{timestamp}.jpg', 'jpeg', use_video_port=True):
    #    pass


    for _, image in enumerate(camera.capture_continuous(raw_capture, format='bgr', use_video_port=True):
        # Get the numpy version of the image.
        decoded_image = image.array
        serialized = pickle.dumps(decoded_image, protocol=0)
        message_producer.publish_message(str(serialized))

capture_images(os.environ['CAPTURE_PATH'])
