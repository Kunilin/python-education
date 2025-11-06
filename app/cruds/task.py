import logging
from typing import List, Optional

from sqlalchemy import select

from app import schemas
from app import models
from sqlalchemy.ext.asyncio import AsyncSession

class TaskCRUD:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def create_task(self, db: AsyncSession, task: schemas.TaskCreate) -> schemas.Task:
        task_db = models.Task(
            title=task.title,
            description=task.description,
            status=task.status,
            user_id=task.user_id
        )

        self.logger.info("Creating task: %s", task)

        db.add(task_db)
        await db.commit()
        await db.refresh(task_db)

        return schemas.Task.model_validate(task_db)

    async def get_tasks(self, db: AsyncSession, user_id: int) -> Optional[List[schemas.Task]]:
        result = await db.execute(
            select(models.Task).filter_by(user_id=user_id)
        )
        tasks = result.scalars().all()
        if not tasks:
            self.logger.info("There is no tasks for such user: %s", user_id)
            return None

        return [schemas.Task.model_validate(task) for task in tasks]

    async def update_task(self, db: AsyncSession, task_id: int, task_update: schemas.TaskUpdate) -> Optional[schemas.Task]:
        results = await db.execute(
            select(models.Task).filter_by(id=task_id)
        )
        task_db = results.scalar_one_or_none()
        if not task_db:
            self.logger.info("There is no such task: %s", task_id)
            return None

        self.logger.info("Updating task: %s", task_id)

        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task_db, field, value)

        await db.commit()
        await db.refresh(task_db)

        return schemas.Task.model_validate(task_db)

    async def delete_task(self, db: AsyncSession, task_id: int) -> schemas.Task:
        results = await db.execute(
            select(models.Task).filter_by(id=task_id)
        )
        task_db = results.scalar_one_or_none()
        if not task_db:
            self.logger.info("There is no such task: %s", task_id)
            return schemas.Task.model_validate(task_db)

        self.logger.info("Deleting task: %s", task_id)

        await db.delete(task_db)
        await db.commit()

        return task_db