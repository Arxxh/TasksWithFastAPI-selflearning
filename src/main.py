from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api import inscription
from core.database import create_db_and_tables
from core.exceptions import AppException


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="estudio, recordando FastAPI",
    summary="basicamente los basics de FastAPI",
    version="1.0",
    lifespan=lifespan,
)


@app.exception_handler(AppException)
async def app_exception_handler(_: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


inscription(app)
