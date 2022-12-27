from sqlalchemy import JSON, Column, String
from sqlalchemy.orm import relationship

from core.db import Base
from core.db.mixins import BaseModelMixin


class AccountRolePermission(Base, BaseModelMixin):
    __tablename__ = "account_role_permission"

    role_name = Column(String(50), unique=True)
    role_permissions = Column(JSON, nullable=False)
    account_users = relationship(
        "AccountUser", back_populates="role", lazy=False
    )
