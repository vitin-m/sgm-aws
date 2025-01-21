from fastapi import APIRouter

from app.api.routes import login
from app.api.routes import user

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(upload.router, prefix="/media", tags=["Media"])