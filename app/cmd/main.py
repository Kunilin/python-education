from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from dotenv import load_dotenv
from sqlalchemy import text

from app.api.endpoints.users import router as users_router
from app.database import create_tables
from app.api.endpoints.tasks import router as tasks_router
from app.kafka.producer import KafkaProducer
from app.logger import setup_logging
from app.test_kafka_consumer import KafkaConsumer

setup_logging()
load_dotenv()

kafka_producer = KafkaProducer()
kafka_consumer = KafkaConsumer()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(fastapi: FastAPI):
    logger.info("Starting application...")

    await create_tables()
    logger.info("Database tables created")

    await kafka_producer.start()
    logger.info("Kafka producer started")

    await kafka_consumer.start()
    logger.info("Kafka consumer started")


    fastapi.state.kafka_producer = kafka_producer
    fastapi.state.kafka_consumer = kafka_consumer
    logger.info("All services started successfully")

    yield # Разделитель для этапов запуска и остановки ресурсов
    logger.info("Shutting down services...")
    await kafka_producer.stop()
    await kafka_consumer.stop()
    logger.info("All services stopped")

app = FastAPI(
    title="Tasks Manger API",
    lifespan=lifespan
    ) # Запуск фастапи с параметрами

app.include_router(tasks_router) # Присобачивание роутера задач к фастапи
app.include_router(users_router) # Присобачивание роутера пользователей к фастапи


@app.get("/")
async def root():
    return {"message": "Tasks Manager API with Kafka"}

# Простенький хелсчек
@app.get("/health")
async def health_check():
    try:
        producer_status = "connected" if kafka_producer.producer else "disconnected"

        consumer_status = "connected" if kafka_consumer.consumer else "disconnected"

        from app.database import engine
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        db_status = "connected"

    except Exception as e:
        db_status = f"disconnected: {str(e)}"

    return {
        "status": "healthy",
        "services": {
            "database": db_status,
            "kafka_producer": producer_status,
            "kafka_consumer": consumer_status
        },
        "timestamp": "2025-11-06T16:00:00Z"
    }