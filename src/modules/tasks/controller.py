from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from core.database import get_session
from modules.tasks.models import Task_Model
from modules.tasks.schemas import TaskCreate
from modules.tasks.service import (
    create_task_service,
    list_tasks_service,
    get_task_service,
    delete_task_service,
)


router = APIRouter(tags=["tasks"])


@router.post(
    "/",
    response_model=Task_Model,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una tarea",
)
async def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    return create_task_service(session, task)


@router.get("/", response_model=list[Task_Model], summary="Obtener todas las tareas")
async def get_tasks(session: Session = Depends(get_session)):
    return list_tasks_service(session)


@router.get("/{task_id}", response_model=Task_Model, summary="Obtener una tarea por ID")
async def get_task(task_id: int, session: Session = Depends(get_session)):
    return get_task_service(session, task_id)


@router.delete("/{task_id}", status_code=status.HTTP_200_OK, summary="Eliminar tarea")
async def delete_task(task_id: int, session: Session = Depends(get_session)):
    delete_task_service(session, task_id)
    return {"message": "Borrado exitoso"}
