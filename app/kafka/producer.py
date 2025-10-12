from aiokafka import AIOKafkaProducer
import os

class KafkaProducer:
    def __init__(self):
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=os.getenv("KAFKA_SERVER"),
        )
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send_task_event(self, event):
        #TODO
        pass
