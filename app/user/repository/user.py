from abc import ABCMeta, abstractmethod
from typing import Optional

from sqlalchemy import or_

from app.user.domain import AccountUser
from core.db import session


class UserRepo:
    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[AccountUser]:
        pass

    @abstractmethod
    async def get_by_email_or_nickname(
        self,
        email: str,
        nickname: str,
    ) -> Optional[AccountUser]:
        pass

    @abstractmethod
    async def save(self, user: AccountUser) -> AccountUser:
        pass

    @abstractmethod
    async def delete(self, user: AccountUser) -> None:
        pass


class UserPostgresRepo(UserRepo):
    async def get_by_id(self, user_id: int) -> Optional[AccountUser]:
        pass

    async def get_by_email_or_nickname(
        self,
        email: str,
        nickname: str,
    ) -> Optional[AccountUser]:
        return (
            session.query(AccountUser)
            .filter(or_(AccountUser.email == email, AccountUser.nickname == nickname))
            .first()
        )

    async def save(self, user: AccountUser) -> AccountUser:
        session.add(user)
        return user

    async def delete(self, user: AccountUser) -> None:
        session.delete(user)
