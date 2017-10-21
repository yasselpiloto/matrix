import logging
import logging.config
import threading

LOGGER = logging.getLogger(__name__)


class Orchestrator(object):
    def __init__(self, message_consumer, message_producer):

        self._message_consumer = message_consumer
        self._message_producer = message_producer
        self._message_consumer.register_message_consumer_callback(self.process_message)

    def start(self):
        producer_thread = threading.Thread(target=self._message_producer.run, args=())
        consumer_thread = threading.Thread(target=self._message_consumer.run, args=())
        producer_thread.start()
        consumer_thread.start()

    def stop(self):
        self._message_consumer.stop()
        self._message_producer.stop()

    def process_message(self, body):
        pass
        #LOGGER.info("consuming message: %s" % body)
