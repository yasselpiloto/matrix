import time
import logging
import pickle
import os
from messaging.AsyncMessageProducer import AsyncMessageProducer
from messaging.AsyncMessageConsumer import AsyncMessageConsumer
from Orchestrator import Orchestrator
import picamera
import picamera.array

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
    message_consumer, message_producer = build_queue_integration()
    orchestrator = Orchestrator(message_consumer, message_producer)
    orchestrator.start()
    with picamera.PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as output:
            camera.resolution = (320, 240)
            camera.vflip = True

            camera.capture(output, 'bgr')
            decoded_image = output.array
            pickle.dump(decoded_image, open("image-pi", "wb"), protocol=0)
            serialized = pickle.dumps(decoded_image, protocol=0)

            time.sleep(0.1)

            message_producer.publish_message(serialized)

            output.truncate(0)


capture_images(os.environ['CAPTURE_PATH'])
