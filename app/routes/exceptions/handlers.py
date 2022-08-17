from starlette.requests import Request

from starlette.responses import JSONResponse
from starlette import status


from app.routes.exceptions.models import CustomException


def custom_exception_handler(
    _: Request,
    exc: CustomException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code or status.HTTP_400_BAD_REQUEST,
        content={**exc.kwargs}
    )