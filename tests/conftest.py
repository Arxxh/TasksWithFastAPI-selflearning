# Configuración global para pruebas de integración
# Este archivo se ejecuta antes que los tests y proporciona fixtures compartidos

from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
from pytest import fixture

from main import app
from core.database import get_session


# Configuración de base de datos de prueba (SQLite en memoria)
# Usamos StaticPool para evitar reconexiones y mejorar performance en tests
@fixture(name="session")
def session_fixture():
    # Crear engine con SQLite en memoria
    # StaticPool evita problemas de conexión en pruebas
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # Crear tablas
    SQLModel.metadata.create_all(engine)

    # Proporcionar sesión para pruebas
    with Session(engine) as session:
        yield session


@fixture(name="client")
def client_fixture(session: Session):
    # Sobrescribir dependencia get_session para usar la sesión de prueba
    def get_session_override():
        return session

    # Crear TestClient con la app de FastAPI
    # El TestClient simula requests HTTP sin levantar un servidor real
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    # Limpiar overrides después del test
    app.dependency_overrides.clear()


@fixture(name="test_task")
def test_task_fixture(session: Session):
    # Datos de prueba para crear una tarea
    # Esto evita repetir código en múltiples tests
    task_data = {"title": "Test Task", "completed": False}
    return task_data
