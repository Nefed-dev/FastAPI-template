from starlette_exporter import PrometheusMiddleware, handle_metrics
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from fastapi import FastAPI

from app.routes.exceptions.binding import setup_exception_handlers
from app.routes.v1.crud_dependencies import crud_dependencies
from app.routes.v1.route_binding import router_v1
from config import settings_app


def get_application_v1() -> FastAPI:
    application = FastAPI(
        debug=False,
        docs_url=None,
        title='BigDealDev',
        version='1.0.0',
        root_path="/api/v1"
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=['*']
    )

    application.include_router(router_v1)

    application.dependency_overrides.update(crud_dependencies)
    application = setup_exception_handlers(app=application)
    # application.middleware('http')(EventLogMiddleware())

    application.add_middleware(
        PrometheusMiddleware,
        app_name="v1",
        skip_paths=['/api/v1/docs', '/api/v1/__metrics'],
    )

    return application



def get_parent_app() -> FastAPI:
    tags_metadata = [
        {
            'name': 'v1',
            "description": "Версия API - v1. Нажмите справа для перехода в документацию",
            'externalDocs': {
                'description': 'дополнительная документация',
                'url': f'https://{settings_app.BASE_DOMAIN}/api/v1/docs'
            }
        },
    ]

    application = FastAPI(
        title='BigDickDev TutorMe API',
        openapi_tags=tags_metadata,
    )

    application.mount("/api/v1", get_application_v1())
    application.add_route("/__metrics", handle_metrics)

    return application


app = get_parent_app()

