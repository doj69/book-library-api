from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def _missing_(cls, name):
        for member in cls:
            if member.name.lower() == name.lower():
                return member


class Role(BaseEnum):
    STUDENT = 1
    LIBRARIAN = 2


class Status(BaseEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class PermissionCode(BaseEnum):
    # * STUDENT
    OPENREAD_OWN_BOOK = "openread.own.books"
    RENEW_BOOKS = "renew.books"

    # * LIBRARIAN
    OPENREAD_STUDENT_BOOKS = "openread.student.books"
    EDIT_BORROWED_BOOKS = "edit.borrowed.books"
    EDIT_RETURNED_BOOKS = "edit.returned.books"
