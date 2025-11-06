import json
import logging
from aiokafka import AIOKafkaProducer
from fastapi import Request
import os
from app.kafka.task_events import EventBase


class KafkaProducer:
    def __init__(self):
        self.producer = None
        self.logger = logging.getLogger(__name__)
        self.bootstrap_server = os.getenv('KAFKA_BOOTSTRAP_SERVER')
        self.topic = os.getenv('KAFKA_TOPIC')

    async def start(self):
        try:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_server,
                value_serializer = lambda v: json.dumps(v).encode('utf-8')
            )
            await self.producer.start()
            self.logger.info("Producer started.")

        except Exception as e:
            self.logger.error(f"Failed to start Kafka producer: {e}")
            raise e

    async def stop(self):
        if self.producer:
            await self.producer.stop()
            self.logger.info("Producer stopped.")

    async def send_task_event(self, event: EventBase):
        try:
            if not self.producer:
                self.logger.warning("Kafka producer not started.")
                return

            event_data = event.model_dump()
            await self.producer.send_and_wait(self.topic, event_data)
            self.logger.info(f"Sent event {event.event_type} to topic {self.topic}")

        except Exception as e:
            self.logger.error(f"Failed to send event {event.event_type}: {e}")

def get_kafka_producer(request: Request) -> KafkaProducer:
    return request.app.state.kafka_producer