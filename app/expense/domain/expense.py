from sqlalchemy import Column, BigInteger, JSON, Float, Date, ForeignKey, Text

from core.db import Base
from core.db.mixins import BaseModelMixin


class Expense(Base, BaseModelMixin):
    __tablename__ = "expenses"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    trx_date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(JSON, ForeignKey("expenses_types.id", ondelete="CASCADE"), nullable=False)
