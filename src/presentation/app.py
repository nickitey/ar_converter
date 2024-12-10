from fastapi import APIRouter, FastAPI

from src.presentation.routers import router


def _create_app(router: APIRouter):
    app = FastAPI(
        title="AR-Converter API",
        description="This service provides online API-converter from different kinds of AR-files to Apple-compartible USDZ-file",
    )

    app.include_router(router)
    return app


app = _create_app(router)
