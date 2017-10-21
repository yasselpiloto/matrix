import logging.config, logging
import os
import time
from datetime import datetime
import picamera
import picamera.array

from messaging.AsyncMessageConsumer import AsyncMessageConsumer
from messaging.AsyncMessageProducer import AsyncMessageProducer

LOGGER = logging.getLogger(__name__)

queue_host_name = "192.168.1.200"
consumer_exchange_name = "matrix"
exchange_type = "topic"
consumer_routing_key = ""
consumer_queue_name = "null"

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

    # Warmup...
    #    time.sleep(2)

    logging.config.fileConfig('config/logging.conf', disable_existing_loggers=False)
    # message_consumer, message_producer = build_queue_integration()
    # orchestrator = Orchestrator(message_consumer, message_producer)
    # orchestrator.start()
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        camera.vflip = True
        while True:
            filename = save_folder + datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f") + '.jpeg'
            print(filename)
            camera.capture(filename, 'jpeg')
            time.sleep(0.2)

            # message_producer.publish_message(serialized)


capture_images(os.environ['CAPTURE_PATH'])
