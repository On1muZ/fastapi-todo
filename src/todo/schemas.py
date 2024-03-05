from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CreateToDo(BaseModel):
    name: str
    text: Optional[str] = None
    time_to_start: Optional[datetime] = None
    time_to_finish: Optional[datetime] = None


class ToDo(BaseModel):
    name: str
    text: Optional[str] = None
    time_to_start: Optional[datetime] = None
    time_to_finish: Optional[datetime] = None
    completed: bool = False


class DeleteToDo(BaseModel):
    user_id: str
    todo_id: str
