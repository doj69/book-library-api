from typing import Optional

from pydantic import BaseModel


class CurrentUser(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None

    class Config:
        validate_assignment = True


class UserRoleSchema(BaseModel):
    id: int
    role_name: str
    role_permissions: list


class CurrentUserSchema(BaseModel):
    id: int
    email: str
    username: str
    status: bool
    role: UserRoleSchema

    class Config:
        validate_assignment = True
