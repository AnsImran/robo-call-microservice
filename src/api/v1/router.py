from fastapi import APIRouter

from src.api.v1.endpoints import call, health

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(call.router)
