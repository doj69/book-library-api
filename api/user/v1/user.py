import logging

from fastapi import APIRouter

from api.user.v1.request import CreateUserRequest
from api.user.v1.response import CreateUserResponse
from app.user.service import UserService
from core.fastapi.schemas.response import ExceptionResponseSchema

user_router = APIRouter()

logger = logging.getLogger(__name__)


@user_router.post(
    "",
    response_model=CreateUserResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
    summary="Create User",
)
async def create_user(request: CreateUserRequest):
    response = await UserService().create_user(**request.dict())

    return response
