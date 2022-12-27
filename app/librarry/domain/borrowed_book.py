from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from core.db import Base
from core.db.mixins import BaseModelMixin


class BorrowedBook(Base, BaseModelMixin):
    __tablename__ = "borrowed_books"
    user_id = Column(
        Integer, ForeignKey("account_user.id", ondelete="RESTRICT")
    )
    book_id = Column(Integer, ForeignKey("books.id", ondelete="RESTRICT"))
    book = relationship("Book")
    returned_date = Column(DateTime, nullable=False)
    is_renewed = Column(Boolean, nullable=False)
    is_returned = Column(Boolean, nullable=False)
