from sqlalchemy import Boolean, Column, Date, String
from sqlalchemy.orm import relationship

from core.db import Base
from core.db.mixins import BaseModelMixin


class Book(Base, BaseModelMixin):
    __tablename__ = "books"
    title = Column(String(255), unique=True, nullable=False)
    author_name = Column(String(255), nullable=False)
    first_publish_date = Column(Date, nullable=False)
    is_available = Column(Boolean, default=False)
    borrowed_record = relationship(
        "BorrowedBook",
        primaryjoin="Book.id == BorrowedBook.book_id",
        order_by="desc(BorrowedBook.returned_date)",
        uselist=False,
        viewonly=True,
    )
