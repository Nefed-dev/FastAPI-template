from fastapi import FastAPI

from app.routes.exceptions.handlers import custom_exception_handler
from app.routes.exceptions.models import CustomException


def setup_exception_handlers(app: FastAPI) -> FastAPI:
    app.add_exception_handler(
        CustomException,
        custom_exception_handler
    )
    # Bind other exceptions here
    return app
