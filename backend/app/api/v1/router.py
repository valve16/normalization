from fastapi import APIRouter

from app.api.v1.endpoints.departments import router as departments_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.roles import router as roles_router
from app.api.v1.endpoints.users import router as users_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(departments_router)
api_router.include_router(roles_router)
api_router.include_router(users_router)
