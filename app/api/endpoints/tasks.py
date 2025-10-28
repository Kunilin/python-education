from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import TaskCRUD

from app import schemas

router = APIRouter(prefix="/tasks")

@router.post("/create", response_model=schemas.Task)
async def create_task(task: schemas.TaskCreate, db: AsyncSession = Depends(get_db)) -> schemas.Task:
    returned_task = await TaskCRUD.create_task(db, task)
    return returned_task
    #TODO
    pass
#TODO: Реализовать остальные ручки тоже