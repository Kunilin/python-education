from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.database import get_db
from app.kafka.producer import KafkaProducer, get_kafka_producer
from app.kafka_service.user_service import UserService

router = APIRouter(prefix="/users")

@router.post("/create", response_model=schemas.User)
async def create_user(
        user: schemas.UserCreate,
        kafka_producer: KafkaProducer = Depends(get_kafka_producer),
        db: AsyncSession = Depends(get_db),
):

    service = UserService()
    returned_user = await service.create_user(db, user, kafka_producer)
    return returned_user

@router.delete("/delete", response_model=schemas.User)
async def delete_user(
        user_id: int,
        kafka_producer: KafkaProducer = Depends(get_kafka_producer),
        db: AsyncSession = Depends(get_db)
):

    service = UserService()
    returned_user = await service.delete_user(user_id, db, kafka_producer)
    return returned_user