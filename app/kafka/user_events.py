# Модели событий
from pydantic import BaseModel

class EventBase(BaseModel):
    event_type:str
    user_id: int
    name: str
    email: str
    timestamp: str

class UserEventCreate(EventBase):
        event_type: str = 'user_create'

class UserEventDelete(EventBase):
        event_type: str = 'user_delete'