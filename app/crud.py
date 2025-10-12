from typing import List

from app import schemas
from sqlalchemy.ext.asyncio import AsyncSession


class TaskCRUD:
    async def create_task(self, db: AsyncSession, task: schemas.TaskCreate) -> schemas.Task:
        #TODO
        pass
    async def get_tasks(self, db: AsyncSession) -> List[schemas.Task]:
        #TODO
        pass
    async def update_task(self, db: AsyncSession, task: schemas.TaskUpdate) -> schemas.Task:
        #TODO
        pass
    async def delete_task(self, db: AsyncSession, task: schemas.Task) -> schemas.Task:
        #TODO
        pass