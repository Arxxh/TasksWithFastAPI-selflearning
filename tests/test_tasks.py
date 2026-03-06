# Pruebas de integración para endpoints de tareas
# Cada test verifica un endpoint específico y su comportamiento

from fastapi import status


def test_create_task(client, test_task):
    """
    Prueba la creación de una tarea (POST /tasks/)
    Verifica:
    1. Código de estado 201 (Created)
    2. Estructura de la respuesta
    3. Datos devueltos coinciden con los enviados
    """
    response = client.post("/tasks/", json=test_task)
    
    # Verificar código de estado
    assert response.status_code == status.HTTP_201_CREATED
    
    # Verificar estructura de respuesta
    data = response.json()
    assert "id" in data
    assert "title" in data
    assert "completed" in data
    
    # Verificar datos
    assert data["title"] == test_task["title"]
    assert data["completed"] == test_task["completed"]


def test_get_tasks_empty(client):
    """
    Prueba obtener todas las tareas cuando no hay ninguna (GET /tasks/)
    Verifica:
    1. Código de estado 200 (OK)
    2. Respuesta es una lista vacía
    """
    response = client.get("/tasks/")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_tasks_with_data(client, test_task):
    """
    Prueba obtener todas las tareas cuando hay datos (GET /tasks/)
    Verifica:
    1. Código de estado 200 (OK)
    2. La tarea creada está en la lista
    """
    # Primero crear una tarea
    client.post("/tasks/", json=test_task)
    
    # Luego obtener todas las tareas
    response = client.get("/tasks/")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Verificar que hay exactamente una tarea
    assert len(data) == 1
    assert data[0]["title"] == test_task["title"]


def test_get_single_task(client, test_task):
    """
    Prueba obtener una tarea específica por ID (GET /tasks/{task_id})
    Verifica:
    1. Código de estado 200 (OK)
    2. Los datos coinciden con los de la tarea creada
    """
    # Crear tarea
    create_response = client.post("/tasks/", json=test_task)
    task_id = create_response.json()["id"]
    
    # Obtener tarea específica
    response = client.get(f"/tasks/{task_id}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["id"] == task_id
    assert data["title"] == test_task["title"]


def test_get_nonexistent_task(client):
    """
    Prueba obtener una tarea que no existe (GET /tasks/{task_id})
    Verifica:
    1. Código de estado 404 (Not Found)
    2. Mensaje de error apropiado
    """
    response = client.get("/tasks/999999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Tarea no encontrada" in response.json()["detail"]


def test_delete_task(client, test_task):
    """
    Prueba eliminar una tarea (DELETE /tasks/{task_id})
    Verifica:
    1. Código de estado 200 (OK)
    2. Mensaje de éxito
    3. La tarea ya no existe en la base de datos
    """
    # Crear tarea
    create_response = client.post("/tasks/", json=test_task)
    task_id = create_response.json()["id"]
    
    # Eliminar tarea
    response = client.delete(f"/tasks/{task_id}")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Borrado exitoso"
    
    # Verificar que la tarea ya no existe
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_nonexistent_task(client):
    """
    Prueba eliminar una tarea que no existe (DELETE /tasks/{task_id})
    Verifica:
    1. Código de estado 404 (Not Found)
    2. Mensaje de error apropiado
    """
    response = client.delete("/tasks/999999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Tarea no encontrada" in response.json()["detail"]