from pydantic import parse_obj_as
from pythondi import inject

from app.user.domain import AccountUser
from app.user.repository import UserRepo
from app.user.schema.user import UserSchema
from core.db import Propagation, Transaction
from core.exceptions.user import (
    PasswordDoesNotMatchException,
    UserNotFoundException,
)
from core.utils.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)


class AuthService:
    @inject()
    def __init__(self, user_repo: UserRepo = UserRepo()):
        self.user_repo = user_repo

    @Transaction(propagation=Propagation.REQUIRED)
    async def login(self, username: str, password: str) -> AccountUser:

        user = await self.user_repo.get_by_username(username=username)
        if not user:
            raise UserNotFoundException

        if not verify_password(password, str(user.hash_password)):
            raise PasswordDoesNotMatchException

        user_schema: UserSchema = parse_obj_as(UserSchema, user)
        access_token = create_access_token({"sub": user_schema.dict()})
        refresh_token = create_refresh_token({"sub": user_schema.dict()})

        update_obj = dict(
            id=user.id,
            access_token=access_token,
            refresh_token=refresh_token,
            updated_by=username,
        )
        await self.user_repo.update(update_obj, user.id)

        return user

    async def user_auth_me(self, id: int):
        user = await self.user_repo.get_by_id(id)

        return user
