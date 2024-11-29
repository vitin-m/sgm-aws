from fastapi import FastAPI

from app.api import api_router
from app.core import settings

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_PATH}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_PATH)
