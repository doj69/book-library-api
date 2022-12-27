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
    async def get_by_email_or_username(
        self,
        email: str,
        username: str,
    ) -> Optional[AccountUser]:
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[AccountUser]:
        pass

    @abstractmethod
    async def save(self, user: dict) -> AccountUser:
        pass

    @abstractmethod
    async def update(self, user: dict, id: int) -> AccountUser:
        pass

    @abstractmethod
    async def delete(self, user: AccountUser) -> None:
        pass


class UserPostgresRepo(UserRepo):
    async def get_by_id(self, user_id: int) -> Optional[AccountUser]:
        result: Optional[AccountUser] = (
            session.query(AccountUser)
            .filter(AccountUser.id == user_id)
            .first()
        )

        return result

    async def get_by_email_or_username(
        self,
        email: str,
        username: str,
    ) -> Optional[AccountUser]:

        result: Optional[AccountUser] = (
            session.query(AccountUser)
            .filter(
                or_(
                    AccountUser.email == email,
                    AccountUser.username == username,
                )
            )
            .first()
        )

        return result

    async def get_by_username(self, username: str) -> Optional[AccountUser]:
        result: Optional[AccountUser] = (
            session.query(AccountUser)
            .filter(
                AccountUser.username == username,
            )
            .first()
        )

        return result

    async def save(self, user: dict) -> AccountUser:
        user_obj = AccountUser(**user)
        session.add(user_obj)
        session.flush()
        return user_obj

    async def update(self, user: dict, id: int) -> AccountUser:
        db_obj_update = session.query(AccountUser).filter(AccountUser.id == id)
        db_obj_update.update(user)

        return db_obj_update.one()

    async def delete(self, user: AccountUser) -> None:
        session.delete(user)
