from datetime import datetime, timedelta

import pytz
from pydantic import parse_obj_as
from pythondi import inject

from app.librarry.repository.book import BookRepo
from app.librarry.schema.book import BookSchema
from core.db.transaction import Propagation, Transaction
from core.exceptions.library import (
    BookNotAvailablexception,
    BookNotFoundException,
    MaxBorrowBookCountException,
)


class BookService:
    @inject()
    def __init__(self, book_repo: BookRepo = BookRepo()):
        self.book_repo = book_repo

    async def book_list(self):
        books = await self.book_repo.available_book_list()
        return books

    async def my_borrow_book(self, user_id: int):
        book = await self.book_repo.student_borrow_books(user_id)

        return book

    async def renew_my_borrow_book(self, username: str, borrow_id: int):
        borrow_book = await self.book_repo.get_borrow_book_by_id(borrow_id)
        if borrow_book:
            book_schema: BookSchema = parse_obj_as(BookSchema, borrow_book)
            if not book_schema.borrowed_record.is_renewed:
                update_obj = dict(
                    is_renewed=True,
                    returned_date=book_schema.borrowed_record.returned_date
                    + timedelta(days=30),
                    updated_by=username,
                )
                await self.book_repo.update_borrow_book(update_obj, borrow_id)

        return borrow_book

    @Transaction(propagation=Propagation.REQUIRED)
    async def mark_as_returned(self, username: str, borrow_id: int):
        borrow_book = await self.book_repo.get_borrow_book_by_id(borrow_id)
        if borrow_book:
            book_schema: BookSchema = parse_obj_as(BookSchema, borrow_book)
            borrow_book_obj = dict(is_returned=True, updated_by=username)
            await self.book_repo.update_borrow_book(borrow_book_obj, borrow_id)
            book_obj = dict(
                is_available=not book_schema.is_available, updated_by=username
            )
            await self.book_repo.update_book(book_obj, book_schema.id)

        return borrow_book

    @Transaction(propagation=Propagation.REQUIRED)
    async def borrow_book(self, current_user, book_id: int, user_id: int):
        book = await self.book_repo.get_book_by_id(book_id)
        borrow_book_count = await self.book_repo.borrow_book_count(user_id)

        if not book:
            raise BookNotFoundException

        if not book.is_available:
            raise BookNotAvailablexception

        if borrow_book_count > 10:
            raise MaxBorrowBookCountException

        book_obj = dict(is_available=False, updated_by=current_user.username)
        await self.book_repo.update_book(book_obj, book_id)

        borrow_obj = dict(
            user_id=user_id,
            book_id=book_id,
            is_renewed=False,
            is_returned=False,
            returned_date=datetime.now(pytz.utc) + timedelta(days=30),
            created_by=current_user.username,
            updated_by=current_user.username,
        )
        await self.book_repo.save_borrow_book(borrow_obj)

        borrow_books = await self.book_repo.student_borrow_books(user_id)

        return borrow_books

    async def student_borrow_books(self, user_id: int):
        borrow_books = await self.book_repo.student_borrow_books(user_id)

        return borrow_books
