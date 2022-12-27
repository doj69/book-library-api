from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from core.db import Base
from core.db.mixins import BaseModelMixin


class AccountUser(Base, BaseModelMixin):
    __tablename__ = "account_user"

    role_id = Column(
        Integer, ForeignKey("account_role_permission.id", ondelete="RESTRICT")
    )
    role = relationship(
        "AccountRolePermission", back_populates="account_users", lazy=False
    )
    username = Column(String(255), unique=True, nullable=False)
    hash_password = Column(String(255), nullable=False)
    temp_password = Column(String(255), nullable=True)
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    fullname = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    register_ip = Column(String(50), nullable=True)
    status = Column(String(50), nullable=False)
    failed_login_attemp = Column(SmallInteger, default=0, nullable=False)
    last_user_agent = Column(String(255), nullable=True)
    last_login_ts = Column(DateTime, nullable=True)
    last_login_ip = Column(String(50), nullable=True)
    last_login_loc = Column(String(50), nullable=True)
