from pythondi import Provider, configure

from app.librarry.repository.book import BookRepo, BookSqlRepo
from app.user.repository import UserPostgresRepo, UserRepo


def init_di():
    provider = Provider()
    provider.bind(UserRepo, UserPostgresRepo)
    provider.bind(BookRepo, BookSqlRepo)
    configure(provider=provider)
