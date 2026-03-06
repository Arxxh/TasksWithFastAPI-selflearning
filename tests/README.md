# Pruebas de Integración para DiagFSAPI

## Estructura

```
tests/
├── __init__.py          # Paquete Python
├── conftest.py         # Configuración global y fixtures
├── test_tasks.py       # Pruebas para endpoints de tareas
└── README.md           # Este archivo
```

## Configuración

### Requisitos
- Python 3.11+
- Virtual environment activado
- Dependencias instaladas (`pytest`, `pytest-cov`)

### Instalación
```bash
# Desde la raíz del proyecto (ESTUDIO/DiagFSAPI/)
source ../.venv/bin/activate
pip install pytest pytest-cov
```

## Ejecución de Pruebas

### Ejecutar todas las pruebas
```bash
python -m pytest tests/ -v
```

### Ejecutar pruebas específicas
```bash
python -m pytest tests/test_tasks.py -v
```

### Ejecutar con cobertura
```bash
python -m pytest tests/test_tasks.py --cov=modules/tasks --cov-report=term-missing -v
```

## Fixtures Disponibles

### `session`
- Proporciona una sesión de base de datos SQLite en memoria
- Crea todas las tablas automáticamente
- Se limpia después de cada test

### `client`
- Proporciona un TestClient de FastAPI configurado
- Sobrescribe la dependencia `get_session` para usar la sesión de prueba
- Permite hacer requests HTTP sin levantar un servidor real

### `test_task`
- Datos de prueba estándar para crear tareas
- Evita repetir código en múltiples tests

## Pruebas Implementadas

### Endpoint: POST /tasks/
- `test_create_task`: Verifica creación exitosa con datos válidos

### Endpoint: GET /tasks/
- `test_get_tasks_empty`: Verifica respuesta vacía cuando no hay tareas
- `test_get_tasks_with_data`: Verifica lista de tareas con datos

### Endpoint: GET /tasks/{task_id}
- `test_get_single_task`: Verifica obtención de tarea específica
- `test_get_nonexistent_task`: Verifica manejo de error 404

### Endpoint: DELETE /tasks/{task_id}
- `test_delete_task`: Verifica eliminación exitosa
- `test_delete_nonexistent_task`: Verifica manejo de error 404

## Cobertura Actual
- **100%** de cobertura en módulo de tareas
- **100%** de cobertura en API

## Buenas Prácticas

1. **Base de datos de prueba**: Usamos SQLite en memoria para no afectar la base de datos de producción
2. **Fixtures**: Configuración reutilizable para evitar código duplicado
3. **Aislamiento**: Cada test corre con una base de datos limpia
4. **Cobertura**: Verificamos que todo el código crítico esté probado
5. **Nomenclatura**: Nombres descriptivos para tests (`test_<acción>_<componente>`)

## Próximos Pasos

- Añadir pruebas para validación de datos (ej: título vacío)
- Implementar pruebas para endpoints de actualización (PATCH/PUT)
- Añadir pruebas de autenticación cuando se implemente
- Configurar CI/CD para ejecutar pruebas automáticamente