from fastapi import APIRouter

from api.user.v1.auth import auth_router
from api.user.v1.user import user_router

sub_router = APIRouter()
sub_router.include_router(user_router, prefix="/api/v1/users", tags=["User"])
sub_router.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])


__all__ = ["sub_router"]
