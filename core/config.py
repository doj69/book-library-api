import os
from typing import Optional

from pydantic import BaseSettings


class Config(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True

    APP_HOST: str = "localhost"
    APP_PORT: int = 8030
    DB_URL: Optional[str] = None

    JWT_SECRET_KEY: str = (
        "3VxUX2uAUkCUSCah8Vl3mwVSy60ScTikyIZT6QkW2nxg3nL9MVXjl0qn_R1GDtIHtw"
    )
    JWT_ALGORITHM: str = "SHA256"

    CELERY_BROKER_URL: str = "amqp://user:bitnami@localhost:5672/"
    CELERY_BACKEND_URL: str = "redis://:password123@localhost:6379/0"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    DATABASE_HOSTNAME: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_PASSWORD: str = "Pass.123"
    DATABASE_NAME: str = "whitelabel"
    DATABASE_USERNAME: str = "postgres"

    SECRET_KEY: str = (
        "6M3ShlTyYUO1A5aZU-xcKwdnpeg2_Wj0StZGhbGtblWge7aVAn-djEifBsumRMmsoQ"
    )
    ALGORITHM: str = "SHA256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 1

    class Config:
        env_file = ".env"


# class DevelopmentConfig(Config):
#     DB_URL: str = f"mysql+pymysql://root:fastapi@db:3306/fastapi"
#     REDIS_HOST: str = "localhost"
#     REDIS_PORT: int = 6379


# class LocalConfig(Config):
#     DB_URL: str = f"mysql+pymysql://fastapi:fastapi@localhost:3306/test"


# class ProductionConfig(Config):
#     DEBUG: str = False
#     DB_URL: str = f"mysql+pymysql://fastapi:fastapi@localhost:3306/prod"


# def get_config():
#     env = os.getenv("ENV", "local")
#     config_type = {
#         "development": DevelopmentConfig(),
#         "local": LocalConfig(),
#         "production": ProductionConfig(),
#     }
#     return config_type[env]


config = Config()
