# Модели событий
from typing import Optional

from pydantic import BaseModel

class EventBase(BaseModel):
    event_type:str
    task_id: int
    title: Optional[str] = None
    status: Optional[str] = None
    user_id: Optional[int] = None
    timestamp: str

class TaskEventCreate(EventBase):
        event_type: str = 'task_create'

class TaskEventUpdate(EventBase):
        event_type: str = 'task_update'

class TasksEventRead(EventBase):
        event_type: str = 'tasks_read'

class TaskEventDelete(EventBase):
        event_type: str = 'task_delete'