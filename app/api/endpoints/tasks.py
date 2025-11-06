from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

from app.schemas import Task, TaskCreate, TaskUpdate
from app.kafka.producer import KafkaProducer, get_kafka_producer
from app.kafka_service.task_service import TaskService

router = APIRouter(prefix="/tasks")

@router.post("/create_task", response_model=Task)
async def create_task(
        task: TaskCreate,
        kafka_producer: KafkaProducer = Depends(get_kafka_producer),
        db: AsyncSession = Depends(get_db)
):

    service = TaskService()
    return await service.create_task(db, task, kafka_producer)

@router.get("/get_tasks", response_model=List[Task])
async def get_tasks(
        user_id: int,
        kafka_producer: KafkaProducer = Depends(get_kafka_producer),
        db: AsyncSession = Depends(get_db)
):

    service = TaskService()

    tasks = await service.get_tasks(user_id, db, kafka_producer)

    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found for such user")
    return tasks

@router.put("/update_task", response_model=Task)
async def update_task(
        task_id: int,
        task: TaskUpdate,
        kafka_producer: KafkaProducer = Depends(get_kafka_producer),
        db: AsyncSession = Depends(get_db)
):

    service = TaskService()

    returned_task = await service.update_task(task_id, db, task, kafka_producer)

    if not returned_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return returned_task

@router.delete("/delete_task")
async def delete_task(
        task_id: int,
        kafka_producer: KafkaProducer = Depends(get_kafka_producer),
        db: AsyncSession = Depends(get_db)
):
    service = TaskService()

    result = await service.delete_task(task_id, db, kafka_producer)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}