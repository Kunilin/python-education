# Настройка DB и SQLAlchemy
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os

engine = create_async_engine(os.getenv("DB_URL"), echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with (AsyncSessionLocal() as session):
        yield session