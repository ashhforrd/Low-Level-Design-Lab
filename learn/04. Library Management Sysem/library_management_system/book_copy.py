from .book import Book
from .enums import BookCopyStatus


class BookCopy:
    def __init__(self, copy_id: str, book: Book) -> None:
        normalized_copy_id = copy_id.strip()

        if normalized_copy_id == "":
            raise ValueError("Copy ID cannot be empty")

        if not isinstance(book, Book):
            raise TypeError("Book must be an instance of Book")

        self.copy_id = normalized_copy_id
        self.book = book
        self.status = BookCopyStatus.AVAILABLE

    def mark_borrowed(self) -> None:
        if self.status not in {
            BookCopyStatus.AVAILABLE,
            BookCopyStatus.RESERVED,
        }:
            raise ValueError(
                "Only AVAILABLE or RESERVED book copies can be borrowed"
            )

        self.status = BookCopyStatus.BORROWED

    def mark_reserved(self) -> None:
        if self.status != BookCopyStatus.AVAILABLE:
            raise ValueError("Only an AVAILABLE book copy can be reserved")

        self.status = BookCopyStatus.RESERVED

    def mark_available(self) -> None:
        if self.status not in {
            BookCopyStatus.BORROWED,
            BookCopyStatus.RESERVED,
        }:
            raise ValueError(
                "Only BORROWED or RESERVED book copies can be marked available"
            )

        self.status = BookCopyStatus.AVAILABLE
