import logging

from sqlalchemy import select

from app import schemas
from app import models
from sqlalchemy.ext.asyncio import AsyncSession

class UserCRUD:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def create_user(self,db: AsyncSession, user: schemas.UserCreate) -> schemas.User:
        user_db = models.User(
            name=user.name,
            email=user.email,
        )

        self.logger.info("Creating user: %s", user)

        db.add(user_db)
        await db.commit()
        await db.refresh(user_db)

        return schemas.User.model_validate(user_db)

    async def delete_user(self,db: AsyncSession, user_id: int) -> schemas.User:
        results = await db.execute(
            select(models.User).filter_by(id=user_id)
        )
        user_db = results.scalar_one_or_none()
        if not user_db:
            self.logger.info("There is no such user: %s", user_id)
            return schemas.User.model_validate(user_db)

        self.logger.info("Deleting user: %s", user_id)

        await db.delete(user_db)
        await db.commit()

        return user_db