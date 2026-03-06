from sqlmodel import SQLModel


class TaskCreate(SQLModel):
    title: str | None = None
    completed: bool = False


class TaskRead(SQLModel):
    id: int
    title: str | None = None
    completed: bool = False


class TaskUpdate(SQLModel):
    title: str | None = None
    completed: bool | None = None
