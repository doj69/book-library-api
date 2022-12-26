from sqlalchemy import Column, BigInteger, String, Text

from core.db import Base
from core.db.mixins import BaseModelMixin


class ExpenseType(Base, BaseModelMixin):
    __tablename__ = "expenses_types"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=False)
