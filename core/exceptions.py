class AppException(Exception):
    status_code = 400
    detail = "Error de aplicación"

    def __init__(self, detail: str | None = None) -> None:
        if detail:
            self.detail = detail


class NotFoundException(AppException):
    status_code = 404
    detail = "Recurso no encontrado"
