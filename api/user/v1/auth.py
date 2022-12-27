import logging

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from api.user.v1.response.user import UserLoginResponse
from app.user.service.auth import AuthService
from core.fastapi.dependencies.permission import (
    IsAuthenticated,
    PermissionDependency,
)
from core.fastapi.schemas.response import ExceptionResponseSchema

auth_router = APIRouter()

logger = logging.getLogger(__name__)


@auth_router.post(
    "/login",
    response_model=UserLoginResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
    summary="User Login",
)
async def user_login(form_data: OAuth2PasswordRequestForm = Depends()):
    response = await AuthService().login(
        form_data.username, form_data.password
    )

    return response


@auth_router.get(
    "/me",
    response_model=UserLoginResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
    summary="Auth Me",
)
async def user_auth_me(request: Request):
    user_id = request.user.id

    if user_id:
        response = await AuthService().user_auth_me(user_id)

        return response
