from core.exceptions import CustomException


class MaxBorrowBookCountException(CustomException):
    code = 400
    error_code = 30000
    message = "The maximum number of books that can be borrowed is 10"


class BookNotFoundException(CustomException):
    code = 400
    error_code = 30001
    message = "Book not found"


class BookNotAvailablexception(CustomException):
    code = 400
    error_code = 30002
    message = "The book not available for borrowed"
