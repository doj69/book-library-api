from datetime import datetime

from pydantic import BaseModel


class BaseUserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "username": "hide",
                "email": "hide@hide.com",
                "created_at": "2021-11-11T07:50:54.289Z",
                "updated_at": "2021-11-11T07:50:54.289Z",
            }
        }


class UserRoleResponse(BaseModel):
    id: int
    role_name: str
    role_permissions: list

    class Config:
        orm_mode = True


class CreateUserResponse(BaseUserResponse):
    pass


class UserLoginResponse(BaseModel):
    id: int
    email: str
    username: str
    status: str
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    role: UserRoleResponse

    class Config:
        orm_mode = True
