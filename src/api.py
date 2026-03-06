from fastapi import FastAPI

from modules.tasks.controller import router as task_router


def inscription(router: FastAPI) -> None:
    router.include_router(task_router, prefix="/tasks")
