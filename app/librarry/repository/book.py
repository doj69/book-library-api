from abc import ABCMeta, abstractmethod
from typing import Optional

from app.librarry.domain.book import Book
from app.librarry.domain.borrowed_book import BorrowedBook
from core.db import session


class BookRepo:
    __metaclass__ = ABCMeta

    @abstractmethod
    async def available_book_list(self) -> list[Book]:
        pass

    @abstractmethod
    async def student_borrow_books(self, user_id: int) -> Optional[Book]:
        pass

    @abstractmethod
    async def update_borrow_book(
        self, borrow_book: dict, borrow_id: int
    ) -> Book:
        pass

    @abstractmethod
    async def get_borrow_book_by_id(self, borrow_id: int) -> Optional[Book]:
        pass

    @abstractmethod
    async def update_book(self, book: dict, book_id: int) -> Book:
        pass

    @abstractmethod
    async def get_book_by_id(self, book_id: int) -> Optional[Book]:
        pass

    @abstractmethod
    async def save_borrow_book(self, borrow_book: dict) -> Book:
        pass

    @abstractmethod
    async def borrow_book_count(self, user_id: int) -> int:
        pass


class BookSqlRepo(BookRepo):
    async def available_book_list(self) -> list[Book]:
        result = session.query(Book).all()

        return result

    async def student_borrow_books(self, user_id: int) -> list[Book]:
        result = (
            session.query(BorrowedBook)
            .filter(
                BorrowedBook.user_id == user_id,
                BorrowedBook.is_returned == False,
            )
            .all()
        )
        return result

    async def update_borrow_book(
        self, borrow_book: dict, borrow_id: int
    ) -> Book:
        db_obj_update = session.query(BorrowedBook).filter(
            BorrowedBook.id == borrow_id
        )
        db_obj_update.update(borrow_book)

        return db_obj_update.one()

    async def get_borrow_book_by_id(self, borrow_id: int) -> Optional[Book]:
        result = (
            session.query(Book).filter(BorrowedBook.id == borrow_id).first()
        )
        return result

    async def update_book(self, book: dict, book_id: int) -> Book:
        db_obj_update = session.query(Book).filter(Book.id == book_id)
        db_obj_update.update(book)

        return db_obj_update.one()

    async def get_book_by_id(self, book_id: int) -> Optional[Book]:
        result = session.query(Book).filter(Book.id == book_id).first()

        return result

    async def save_borrow_book(self, borrow_book: dict) -> Book:
        borrow_book_obj = BorrowedBook(**borrow_book)
        session.add(borrow_book_obj)
        session.flush()

        return borrow_book_obj

    async def borrow_book_count(self, user_id: int) -> int:
        result = (
            session.query(BorrowedBook)
            .filter(BorrowedBook.user_id == user_id)
            .count()
        )
        return result
