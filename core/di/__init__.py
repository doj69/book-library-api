from pythondi import Provider, configure
from app.user.repository import UserRepo, UserPostgresRepo


def init_di():
    provider = Provider()
    provider.bind(UserRepo, UserPostgresRepo)
    configure(provider=provider)
