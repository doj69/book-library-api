from pydantic import BaseModel

from core.enums import Role


class CreateUserRequest(BaseModel):
    email: str
    username: str
    password: str
    role: Role

    class Config:
        schema_extra = {
            "example": {
                "email": "hide@hide.com",
                "username": "hide",
                "password": "password",
                "role": "role",
            }
        }


# class UserLoginRequest(BaseModel):
#     username: str
#     password: str

#     class Config:
#         schema_extra = {
#             "example": {
#                 "username": "hide",
#                 "password": "password",
#             }
#         }
