from fastapi import APIRouter

from api.library.v1.book import book_router

sub_router = APIRouter()
sub_router.include_router(book_router, prefix="/api/v1/books", tags=["Book"])


__all__ = ["sub_router"]
