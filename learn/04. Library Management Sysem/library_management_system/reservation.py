from datetime import datetime
from typing import Optional

from .book_copy import BookCopy
from .member import Member
from .book import Book
from .enums import ReservationStatus


class Reservation:
    def __init__(
        self,
        reservation_id: str,
        member: Member,
        book: Book,
        reserved_at: datetime,
    ) -> None:
        normalized_reservation_id = reservation_id.strip()

        if normalized_reservation_id == "":
            raise ValueError("reservation_id cannot be empty")

        if not isinstance(member, Member):
            raise TypeError("member must be an instance of Member")

        if not isinstance(book, Book):
            raise TypeError("book must be an instance of Book")

        if not isinstance(reserved_at, datetime):
            raise TypeError("reserved_at must be an instance of datetime")

        self.reservation_id = normalized_reservation_id
        self.member = member
        self.book = book
        self.reserved_at = reserved_at
        self.status = ReservationStatus.WAITING
        self.book_copy: Optional[BookCopy] = None

    def allocate_copy(self, book_copy: BookCopy) -> None:
        if self.status != ReservationStatus.WAITING:
            raise ValueError("Only WAITING status can be allocated")

        if not isinstance(book_copy, BookCopy):
            raise TypeError("book_copy must be an instance of BookCopy")

        if book_copy.book != self.book:
            raise ValueError("book_copy must belong to the reserved book")

        self.book_copy = book_copy
        self.status = ReservationStatus.READY

    def complete(self) -> None:
        if self.status != ReservationStatus.READY:
            raise ValueError("Only READY status can be completed")

        if self.book_copy is None:
            raise ValueError("READY reservation must have an allocated book copy")

        self.status = ReservationStatus.COMPLETED

    def cancel(self) -> None:
        if self.status in {
            ReservationStatus.COMPLETED,
            ReservationStatus.CANCELLED,
        }:
            raise ValueError(
                "Cannot cancel a reservation that is already completed or cancelled"
            )

        self.status = ReservationStatus.CANCELLED
