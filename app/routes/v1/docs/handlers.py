from fastapi import APIRouter

from app.swagger.render import custom_swagger_ui_html

docs_router = APIRouter()


@docs_router.get("/docs", include_in_schema=False)
async def docs_handler():
    """
    Ручка на сваггер
    """
    return custom_swagger_ui_html(openapi_url="openapi.json", title="Документация")
