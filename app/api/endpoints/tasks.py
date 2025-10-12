from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

from app import schemas

router = APIRouter(prefix="/tasks")

@router.post("/create", response_model=schemas.Task)
async def create_task(task: schemas.TaskCreate, db: AsyncSession = Depends(get_db)) -> schemas.Task:
    #TODO
    pass
#TODO: Реализовать остальные ручки тоже