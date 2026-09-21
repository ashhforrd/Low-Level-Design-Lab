from datetime import datetime
from typing import Optional

from .member import Member
from .book_copy import BookCopy
from .enums import LoanStatus


class Loan:
    def __init__(
        self,
        loan_id: str,
        member: Member,
        book_copy: BookCopy,
        borrowed_at: datetime,
        due_at: datetime,
    ) -> None:
        normalized_loan_id = loan_id.strip()

        if normalized_loan_id == "":
            raise ValueError("Loan ID cannot be empty")

        if not isinstance(member, Member):
            raise TypeError("member must be an instance of Member")

        if not isinstance(book_copy, BookCopy):
            raise TypeError("book_copy must be an instance of BookCopy")

        if not isinstance(borrowed_at, datetime):
            raise TypeError("borrowed_at must be an instance of datetime")

        if not isinstance(due_at, datetime):
            raise TypeError("due_at must be an instance of datetime")

        if due_at <= borrowed_at:
            raise ValueError("due_at must be later than borrowed_at")

        self.loan_id = normalized_loan_id
        self.member = member
        self.book_copy = book_copy
        self.borrowed_at = borrowed_at
        self.due_at = due_at
        self.returned_at: Optional[datetime] = None
        self.status = LoanStatus.ACTIVE

    def complete(self, returned_at: datetime) -> None:
        if self.status != LoanStatus.ACTIVE:
            raise ValueError("Only ACTIVE status can be completed")

        if not isinstance(returned_at, datetime):
            raise TypeError("returned_at must be an instance of datetime")

        if returned_at < self.borrowed_at:
            raise ValueError("returned_at cannot be earlier than borrowed_at")

        self.returned_at = returned_at
        self.status = LoanStatus.RETURNED

    def is_overdue(self, current_time: datetime) -> bool:
        if not isinstance(current_time, datetime):
            raise TypeError("current_time must be an instance of datetime")

        return self.status == LoanStatus.ACTIVE and current_time > self.due_at
