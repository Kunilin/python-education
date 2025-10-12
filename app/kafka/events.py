# Модели событий
from datetime import datetime

from pydantic import BaseModel

class Event(BaseModel):
    event_type:str
    id: int
    title: str
    status: str
    user_id: int
    timestamp: datetime