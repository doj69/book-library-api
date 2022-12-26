import logging

from api.user.v1.request import CreateUserRequest, UpdatePasswordRequest
from api.user.v1.response import CreateUserResponse, GetUserResponse
from app.user.service import UserService
from core.exceptions.base import BadRequestException
from core.fastapi.dependencies import IsAdmin, PermissionDependency
from core.fastapi.schemas.response import ExceptionResponseSchema
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

user_router = APIRouter()

logger = logging.getLogger(__name__)


@user_router.post(
    "",
    response_model=CreateUserResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
    summary="Create User",
)
async def create_user(request: CreateUserRequest):
    return await UserService().create_user(**request.dict())


@user_router.get(
    "/{user_id}",
    response_model=GetUserResponse,
    responses={"404": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
    summary="Get User",
)
async def get_user(user_id: int):
    return await UserService().get_user(user_id=user_id)


@user_router.put(
    "/{user_id}/password",
    responses={"404": {"model": ExceptionResponseSchema}},
    summary="Change User Password",
)
async def update_password(request: UpdatePasswordRequest, user_id: int):
    await UserService().update_password(
        user_id=user_id,
        password1=request.password1,
        password2=request.password2,
    )


@user_router.get(
    "test-logging",
    responses={"404": {"model": ExceptionResponseSchema}},
    summary="Test Logging",
)
async def logging_test():
    for x in range(0, 10000):
        try:

            logger.info("Test info")
            logger.warning("Test warning")
            logger.error("Test error")
            logger.critical("Test critical")
            raise Exception("test logging exception")
        except Exception as e:
            logger.error(str(e), exc_info=True)
            continue
