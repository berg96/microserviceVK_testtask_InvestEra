from fastapi import APIRouter

from app.api.endpoints import auth_router, users_router

main_router = APIRouter()
main_router.include_router(
    auth_router, prefix='/auth', tags=['Authentication']
)
main_router.include_router(
    users_router, prefix='/users', tags=['Users']
)
