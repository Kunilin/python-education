import asyncio
import os

from fastapi import FastAPI
from dotenv import load_dotenv
from app.database import create_tables

load_dotenv()
from api.endpoints.tasks import router


asyncio.run(create_tables()) # Создаем таблицы
app = FastAPI(title="Tasks Manger API") # Запуск фастапи
app.include_router(router) # Присобачивание роутера к фастапи