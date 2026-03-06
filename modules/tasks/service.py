from sqlmodel import Session, select

from core.exceptions import NotFoundException
from modules.tasks.models import Task_Model
from modules.tasks.schemas import TaskCreate


def create_task_service(session: Session, task: TaskCreate) -> Task_Model:
    db_task = Task_Model.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def list_tasks_service(session: Session) -> list[Task_Model]:
    return session.exec(select(Task_Model)).all()


def get_task_service(session: Session, task_id: int) -> Task_Model:
    task = session.get(Task_Model, task_id)
    if not task:
        raise NotFoundException("Tarea no encontrada")
    return task


def delete_task_service(session: Session, task_id: int) -> None:
    task = session.get(Task_Model, task_id)
    if not task:
        raise NotFoundException("Tarea no encontrada")
    session.delete(task)
    session.commit()
