import time
import logging
import pickle
import os
from messaging.AsyncMessageProducer import AsyncMessageProducer
from messaging.AsyncMessageConsumer import AsyncMessageConsumer
from Orchestrator import Orchestrator
from picamera import PiCamera
from picamera.array import PiRGBArray

LOGGER = logging.getLogger(__name__)

queue_host_name = "192.168.1.200"
consumer_exchange_name = "matrix"
exchange_type = "topic"
consumer_routing_key = ""
consumer_queue_name = "image_input"
producer_exchange_name = "matrix"
producer_routing_key = ""
producer_queue_name = "image_input"


def build_queue_integration():

    message_consumer = AsyncMessageConsumer(queue_host_name, consumer_exchange_name,
                                            exchange_type, consumer_routing_key,
                                            consumer_queue_name)

    message_producer = AsyncMessageProducer(queue_host_name, producer_exchange_name,
                                            exchange_type, producer_routing_key,
                                            producer_queue_name)
    return message_consumer, message_producer

def capture_images(save_folder):
    """Stream images off the camera and save them."""
    camera = PiCamera()
    camera.resolution = (320, 240)
    camera.vflip = True
    camera.framerate = 10
    raw_capture = PiRGBArray(camera, size=(320, 240))

    # Warmup...
    time.sleep(2)

    # And capture continuously forever.
    #for _ in camera.capture_continuous(save_folder + '{timestamp}.jpg', 'jpeg', use_video_port=True):
    #    pass

    logging.config.fileConfig('config/logging.conf', disable_existing_loggers=False)
    message_consumer, message_producer = build_queue_integration()
    orchestrator = Orchestrator(message_consumer, message_producer)
    orchestrator.start()

    for _, image in enumerate(camera.capture_continuous(raw_capture, format='bgr', use_video_port=True)):
        # Get the numpy version of the image.
        decoded_image = image.array
        serialized = pickle.dumps(decoded_image, protocol=0)
        message_producer.publish_message(str(serialized))

capture_images(os.environ['CAPTURE_PATH'])
