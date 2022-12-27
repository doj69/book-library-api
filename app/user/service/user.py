from typing import NoReturn, Optional, Union

from pydantic import parse_obj_as
from pythondi import inject

from app.user.domain import AccountUser
from app.user.repository import UserRepo
from app.user.schema.user import UserSchema
from core.db import Propagation, Transaction
from core.enums import Role, Status
from core.exceptions.user import (
    DuplicateEmailOrUsernameException,
    UserNotFoundException,
)
from core.utils.security import hash_password


class UserService:
    @inject()
    def __init__(self, user_repo: UserRepo = UserRepo()):
        self.user_repo = user_repo

    @Transaction(propagation=Propagation.REQUIRED)
    async def create_user(
        self, email: str, username: str, password: str, role: Role
    ) -> Union[AccountUser, NoReturn]:

        existing_user = await self.user_repo.get_by_email_or_username(
            email=email, username=username
        )
        if existing_user:
            raise DuplicateEmailOrUsernameException

        insert_obj = dict(
            email=email,
            username=username,
            hash_password=hash_password(password),
            temp_password=hash_password(password),
            role_id=role.value,
            status=Status.ACTIVE.value,
        )
        user = await self.user_repo.save(user=insert_obj)
        return user

    async def is_role_permissions_granted(
        self, user_id: int, allowed_permission: str
    ) -> bool:

        user = await self.user_repo.get_by_id(user_id=user_id)
        user_schema: UserSchema = parse_obj_as(UserSchema, user)

        if not user:
            return False

        if allowed_permission not in user_schema.role.role_permissions:
            return False

        return True

    async def get_user(self, user_id: int) -> Optional[AccountUser]:
        user = await self.user_repo.get_by_id(user_id=user_id)
        if not user:
            raise UserNotFoundException

        return user
