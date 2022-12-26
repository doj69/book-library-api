from sqlalchemy import Column, DateTime, Integer, func, String
from sqlalchemy.ext.declarative import declared_attr


class BaseModelMixin:
    @declared_attr
    def id(cls):
        return Column(Integer, primary_key=True, index=True)

    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=func.now(), nullable=False)

    @declared_attr
    def created_by(cls):
        return Column(String, default="system", nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime,
            default=func.now(),
            onupdate=func.now(),
            nullable=False,
        )

    @declared_attr
    def updated_by(cls):
        return Column(
            String,
            default="system",
            nullable=False,
        )
