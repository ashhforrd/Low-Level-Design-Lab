from datetime import datetime
from uuid import uuid4

from .book import Book
from .book_copy import BookCopy
from .member import Member
from .loan import Loan
from .reservation import Reservation
from .enums import BookCopyStatus, ReservationStatus


class LibrarySystem:
    def __init__(self) -> None:
        self.books: dict[str, Book] = {}
        self.book_copies: dict[str, BookCopy] = {}
        self.members: dict[str, Member] = {}
        self.loans: dict[str, Loan] = {}
        self.reservations: dict[str, Reservation] = {}

    def add_book(self, book: Book) -> None:
        if not isinstance(book, Book):
            raise TypeError("book must be an instance of Book")

        if book.isbn in self.books:
            raise ValueError(f"Book with ISBN {book.isbn} already exists")

        self.books[book.isbn] = book

    def add_book_copy(self, book_copy: BookCopy) -> None:
        if not isinstance(book_copy, BookCopy):
            raise TypeError("book_copy must be an instance of BookCopy")

        if book_copy.copy_id in self.book_copies:
            raise ValueError(f"Book copy with ID {book_copy.copy_id} already exists")

        if book_copy.book.isbn not in self.books:
            raise ValueError(
                f"Book with ISBN {book_copy.book.isbn} is not registered"
            )

        self.book_copies[book_copy.copy_id] = book_copy
        self.allocate_available_copy(book_copy)

    def add_member(self, member: Member) -> None:
        if not isinstance(member, Member):
            raise TypeError("member must be an instance of Member")

        if member.member_id in self.members:
            raise ValueError(
                f"Member with ID {member.member_id} is already registered"
            )

        self.members[member.member_id] = member

    def borrow_book(
        self,
        member_id: str,
        copy_id: str,
        borrowed_at: datetime,
        due_at: datetime,
    ) -> Loan:
        member = self.members.get(member_id)

        if member is None:
            raise ValueError(f"Member with ID {member_id} was not found")

        book_copy = self.book_copies.get(copy_id)

        if book_copy is None:
            raise ValueError(f"Book copy with ID {copy_id} was not found")

        if book_copy.status != BookCopyStatus.AVAILABLE:
            raise ValueError("Book copy is not available")

        loan_id = str(uuid4())
        loan = Loan(
            loan_id,
            member,
            book_copy,
            borrowed_at,
            due_at,
        )

        book_copy.mark_borrowed()

        self.loans[loan_id] = loan

        return loan

    def return_book(self, loan_id: str, returned_at: datetime) -> None:
        loan = self.loans.get(loan_id)

        if loan is None:
            raise ValueError(f"Loan with ID {loan_id} was not found")

        loan.complete(returned_at)
        loan.book_copy.mark_available()

        self.allocate_available_copy(loan.book_copy)

    def reserve_book(
        self,
        member_id: str,
        isbn: str,
        reserved_at: datetime,
    ) -> Reservation:
        member = self.members.get(member_id)

        if member is None:
            raise ValueError(f"Member with ID {member_id} was not found")

        book = self.books.get(isbn)

        if book is None:
            raise ValueError(f"Book with ISBN {isbn} was not found")

        has_available_copy = any(
            book_copy.book.isbn == isbn
            and book_copy.status == BookCopyStatus.AVAILABLE
            for book_copy in self.book_copies.values()
        )

        if has_available_copy:
            raise ValueError(
                "Book is currently available and does not need to be reserved"
            )

        has_active_reservation = any(
            reservation.member.member_id == member_id
            and reservation.book.isbn == isbn
            and reservation.status in {
                ReservationStatus.WAITING,
                ReservationStatus.READY,
            }
            for reservation in self.reservations.values()
        )

        if has_active_reservation:
            raise ValueError(
                "Member already has an active reservation for this book"
            )

        reservation_id = str(uuid4())
        reservation = Reservation(
            reservation_id,
            member,
            book,
            reserved_at,
        )
        self.reservations[reservation_id] = reservation
        return reservation

    def borrow_reserved_book(
        self,
        reservation_id: str,
        borrowed_at: datetime,
        due_at: datetime,
    ) -> Loan:
        reservation = self.reservations.get(reservation_id)

        if reservation is None:
            raise ValueError(f"Reservation with ID {reservation_id} was not found")

        if reservation.status != ReservationStatus.READY:
            raise ValueError("Only a READY reservation can be borrowed")

        if reservation.book_copy is None:
            raise ValueError("READY reservation must have an allocated book copy")

        book_copy = reservation.book_copy

        if book_copy.status != BookCopyStatus.RESERVED:
            raise ValueError(
                "The allocated book copy must have RESERVED status"
            )

        loan_id = str(uuid4())
        loan = Loan(
            loan_id,
            reservation.member,
            book_copy,
            borrowed_at,
            due_at,
        )

        book_copy.mark_borrowed()
        reservation.complete()

        self.loans[loan_id] = loan
        return loan

    def cancel_reservation(self, reservation_id: str) -> None:
        reservation = self.reservations.get(reservation_id)

        if reservation is None:
            raise ValueError(f"Reservation with ID {reservation_id} was not found")

        book_copy = reservation.book_copy

        reservation.cancel()

        if book_copy is None:
            return

        book_copy.mark_available()

        self.allocate_available_copy(book_copy)

    def allocate_available_copy(self, book_copy: BookCopy) -> None:
        if book_copy.status != BookCopyStatus.AVAILABLE:
            raise ValueError("Only an AVAILABLE book copy can be allocated")

        waiting_reservations = [
            reservation
            for reservation in self.reservations.values()
            if reservation.status == ReservationStatus.WAITING
            and reservation.book == book_copy.book
        ]

        if not waiting_reservations:
            return

        next_reservation = min(
            waiting_reservations,
            key=lambda reservation: reservation.reserved_at,
        )

        book_copy.mark_reserved()
        next_reservation.allocate_copy(book_copy)

    def search_books(self, query: str) -> list[Book]:
        normalized_query = query.strip().lower()

        if normalized_query == "":
            raise ValueError("Query cannot be empty")

        return [
            book
            for book in self.books.values()
            if normalized_query in book.isbn.lower()
            or normalized_query in book.title.lower()
            or normalized_query in book.author.lower()
        ]

    def remove_book_copy(self, copy_id: str) -> BookCopy:
        book_copy = self.book_copies.get(copy_id)

        if book_copy is None:
            raise ValueError(f"Book copy with ID {copy_id} was not found")

        if book_copy.status != BookCopyStatus.AVAILABLE:
            raise ValueError("Only an AVAILABLE book copy can be removed")

        return self.book_copies.pop(copy_id)
