import logging

from fastapi import APIRouter, Depends, Request

from api.library.v1.response.book import BookResponse, BorrowBookResponse
from app.librarry.service.book import BookService
from core.enums import PermissionCode
from core.fastapi.dependencies.permission import (
    IsRolePermissionGranted,
    PermissionDependency,
)
from core.fastapi.schemas.response import ExceptionResponseSchema

book_router = APIRouter()

logger = logging.getLogger(__name__)


@book_router.get(
    "",
    response_model=list[BookResponse],
    responses={"400": {"model": ExceptionResponseSchema}},
    summary="Book List",
)
async def book_list():
    response = await BookService().book_list()

    return response


@book_router.get(
    "/borrow",
    response_model=list[BorrowBookResponse],
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[
        Depends(
            PermissionDependency(
                [IsRolePermissionGranted],
                PermissionCode.OPENREAD_OWN_BOOK.value,
            )
        )
    ],
    summary="My Borrow Book",
)
async def my_borrow_book(request: Request):
    user_id: int = request.user.id

    response = await BookService().my_borrow_book(user_id)

    return response


@book_router.post(
    "/borrow",
    response_model=list[BorrowBookResponse],
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[
        Depends(
            PermissionDependency(
                [IsRolePermissionGranted],
                PermissionCode.EDIT_BORROWED_BOOKS.value,
            )
        )
    ],
    summary="Borrow Book Process",
)
async def borrow_book(request: Request, book_id: int, user_id: int):
    current_user = request.user

    response = await BookService().borrow_book(current_user, book_id, user_id)

    return response


@book_router.put(
    "/borrow/renew",
    response_model=BookResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[
        Depends(
            PermissionDependency(
                [IsRolePermissionGranted],
                PermissionCode.RENEW_BOOKS.value,
            )
        )
    ],
    summary="Renew my Borrow Book",
)
async def renew_borrow_book(request: Request, borrow_id: int):
    username: str = request.user.username

    response = await BookService().renew_my_borrow_book(username, borrow_id)

    return response


@book_router.put(
    "/borrow/returned",
    response_model=BookResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[
        Depends(
            PermissionDependency(
                [IsRolePermissionGranted],
                PermissionCode.EDIT_RETURNED_BOOKS.value,
            )
        )
    ],
    summary="Mark as returned by librarian",
)
async def mark_as_returned(request: Request, borrow_id: int):
    username: str = request.user.username

    response = await BookService().mark_as_returned(username, borrow_id)

    return response


@book_router.get(
    "/history",
    response_model=list[BorrowBookResponse],
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[
        Depends(
            PermissionDependency(
                [IsRolePermissionGranted],
                PermissionCode.OPENREAD_STUDENT_BOOKS.value,
            )
        )
    ],
    summary="History of Borrowing",
)
async def history_borrowing(user_id: int):
    response = await BookService().student_borrow_books(user_id)

    return response
