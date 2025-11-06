import asyncio
import json
import logging
import os

from aiokafka import AIOKafkaConsumer
from dotenv import load_dotenv

load_dotenv()

class KafkaConsumer:
    def __init__(self):
        self.consumer = None
        self.logger = logging.getLogger(__name__)
        self.kafka_topic = os.getenv("KAFKA_TOPIC")
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVER")
        self._consuming_task = None

    async def start(self):
        try:
            self.consumer = AIOKafkaConsumer(
                self.kafka_topic,
                bootstrap_servers=self.bootstrap_servers,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            )
            await self.consumer.start()
            self.logger.info("Kafka consumer started.")
            self._consuming_task = asyncio.create_task(self._consume_messages())

        except Exception as e:
            self.logger.error(f"Failed to start Kafka consumer: {e}")
            raise e

    async def _consume_messages(self):
        """Фоновая задача для потребления сообщений (не блокирует основной поток)"""
        try:
            self.logger.info("👂 Kafka consumer started listening for messages...")
            async for msg in self.consumer:
                print(f"📨 Received message: {msg.value}")
                self.logger.info(f"📨 Received Kafka message: {msg.value}")
        except Exception as e:
            self.logger.error(f"❌ Error in Kafka consumer: {e}")

    async def stop(self):
        if self._consuming_task:

            self._consuming_task.cancel()
            try:
                await self._consuming_task
            except Exception as e:
                self.logger.error(f"Failed to stop Kafka consumer: {e}")

        if self.consumer:
            await self.consumer.stop()
            self.logger.info("Kafka consumer stopped.")

    async def consume(self):
        async for message in self.consumer:
            message = json.loads(message.value)
            self.logger.info(f"Received message: {message}")
