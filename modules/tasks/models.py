from sqlmodel import SQLModel, Field
from typing import Optional


class Task_Model(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    completed: bool = False
