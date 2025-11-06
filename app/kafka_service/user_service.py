import logging
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds.user import UserCRUD
from app.kafka.user_events import UserEventCreate, UserEventDelete
from app.schemas import UserCreate, User
from app.kafka.producer import KafkaProducer


class UserService:
    def __init__(self):
        self.crud = UserCRUD()
        self.logger = logging.getLogger(__name__)

    async def create_user(
            self,
            db: AsyncSession,
            user_data: UserCreate,
            kafka_producer: KafkaProducer,
    ) -> User:

        user = await self.crud.create_user(db, user_data)

        user_event = UserEventCreate(
            user_id=user.id,
            name=user.name,
            email=user.email,
            timestamp=datetime.now().isoformat(),
        )

        await kafka_producer.send_task_event(user_event)
        self.logger.info(f"User {user.id} created and event sent to Kafka")

        return user

    async def delete_user(
            self,
            user_id: int,
            db: AsyncSession,
            kafka_producer: KafkaProducer,
    ) -> User:
        user = await self.crud.delete_user(db, user_id)

        user_event = UserEventDelete(
            user_id=user_id,
            name=user.name,
            email=user.email,
            timestamp=datetime.now().isoformat()
        )

        await kafka_producer.send_task_event(user_event)
        self.logger.info(f"User {user_id} deleted and event sent to Kafka")

        return user