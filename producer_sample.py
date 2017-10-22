import logging
from messaging.AsyncMessageProducer import AsyncMessageProducer
from messaging.AsyncMessageConsumer import AsyncMessageConsumer
from Orchestrator import Orchestrator


LOGGER = logging.getLogger(__name__)

queue_host_name = "192.168.1.200"
consumer_exchange_name = "matrix"
exchange_type = "topic"
consumer_routing_key = ""
consumer_queue_name = "image_input"
producer_exchange_name = "matrix"
producer_routing_key = "cart_events_key"
producer_queue_name = "cart_events"

def build_queue_integration():

    message_consumer = AsyncMessageConsumer(queue_host_name, consumer_exchange_name,
                                            exchange_type, consumer_routing_key,
                                            consumer_queue_name)

    message_producer = AsyncMessageProducer(queue_host_name, producer_exchange_name,
                                            exchange_type, producer_routing_key,
                                            producer_queue_name)
    return message_consumer, message_producer

if __name__ == "__main__":
    logging.config.fileConfig('config/logging.conf', disable_existing_loggers=False)
    message_consumer, message_producer = build_queue_integration()
    orchestrator = Orchestrator(message_consumer, message_producer)
    orchestrator.start()
    for i in range(10):
        message_producer.publish_message("add,1")

    message_producer.publish_message("checkout")
