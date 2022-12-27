from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class BookBase(BaseModel):
    id: int
    title: str
    author_name: str
    first_publish_date: date
    is_available: bool

    class Config:
        orm_mode = True


class BorrowedBookBase(BaseModel):
    id: int
    returned_date: datetime
    is_renewed: bool
    is_returned: bool

    class Config:
        orm_mode = True


class BorrowerBase(BaseModel):
    id: int
    username: str


class BookResponse(BookBase):
    # borrower: Optional[BorrowerBase]
    borrowed_record: Optional[BorrowedBookBase]

    class Config:
        orm_mode = True


class BorrowBookResponse(BorrowedBookBase):
    book: BookBase
