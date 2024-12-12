from fastapi import APIRouter, FastAPI

from src.core.settings import Settings
from src.presentation.routers import router


def _create_app(router: APIRouter):
    settings = Settings()
    app = FastAPI(
        title="AR-Converter API",
        description="This service provides online API-converter from different kinds of AR-files to Apple-compartible USDZ-file",
        docs_url="/docs" if settings.app.mount_swagger else None,
        redoc_url="/redoc" if settings.app.mount_redoc else None,
        openapi_url="/openapi.json" if settings.app.mount_swagger or settings.app.mount_redoc else None

    )

    app.include_router(router)
    return app


app = _create_app(router)
