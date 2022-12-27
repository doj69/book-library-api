from pydantic import BaseModel


class UserRoleSchema(BaseModel):
    id: int
    role_name: str
    role_permissions: list

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    id: int
    email: str
    username: str
    status: str
    role: UserRoleSchema

    class Config:
        orm_mode = True
