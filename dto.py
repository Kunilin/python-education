from datetime import datetime


class Task:
    def __init__(self, task_id:int, title:str, description:str, status:str,created_at:datetime, updated_at:datetime, user_id:int):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.user_id = user_id