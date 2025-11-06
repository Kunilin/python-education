import logging
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds.task import TaskCRUD
from app.kafka.task_events import TaskEventCreate, TaskEventUpdate, TaskEventDelete, TasksEventRead
from app.schemas import TaskCreate, Task, TaskUpdate
from app.kafka.producer import KafkaProducer


class TaskService:
    def __init__(self):
        self.crud = TaskCRUD()
        self.logger = logging.getLogger(__name__)

    async def create_task(
            self,
            db: AsyncSession,
            task_data: TaskCreate,
            kafka_producer: KafkaProducer,
    ) -> Task:

        task = await self.crud.create_task(db, task_data)

        task_event = TaskEventCreate(
            task_id=task.id,
            title=task.title,
            status=task.status,
            user_id=task.user_id,
            timestamp=datetime.now().isoformat(),
        )

        await kafka_producer.send_task_event(task_event)
        self.logger.info(f"Task {task.id} created and event sent to Kafka")

        return task

    async def update_task(
            self,
            task_id: int,
            db: AsyncSession,
            task_data: TaskUpdate,
            kafka_producer: KafkaProducer,
    ) -> Task:
        task = await self.crud.update_task(db, task_id, task_data)

        task_event = TaskEventUpdate(
            task_id=task.id,
            title=task.title,
            status=task.status,
            user_id=task.user_id,
            timestamp=datetime.now().isoformat(),
        )

        await kafka_producer.send_task_event(task_event)
        self.logger.info(f"Task {task.id} updated and event sent to Kafka")

        return task

    async def get_tasks(
            self,
            user_id: int,
            db: AsyncSession,
            kafka_producer: KafkaProducer,
    ) -> list[Task]:

        tasks = await self.crud.get_tasks(db,user_id)

        if not tasks:
            self.logger.info("There is no tasks for such user: %s", user_id)
            return []

        for task in tasks:

            task_event = TasksEventRead(
            task_id=task.id,
            title=task.title,
            status=task.status,
            user_id=task.user_id,
            timestamp=datetime.now().isoformat(),
            )

            await kafka_producer.send_task_event(task_event)
            self.logger.info(f"Task {task.id} was read and event sent to Kafka")

        return tasks

    async def delete_task(
            self,
            task_id: int,
            db: AsyncSession,
            kafka_producer: KafkaProducer,
    ) -> bool:
        is_deleted = await self.crud.delete_task(db, task_id)

        task_event = TaskEventDelete(
            task_id=task_id,
            timestamp=datetime.now().isoformat()
        )

        await kafka_producer.send_task_event(task_event)
        self.logger.info(f"Task {task_id} deleted and event sent to Kafka")

        return is_deleted