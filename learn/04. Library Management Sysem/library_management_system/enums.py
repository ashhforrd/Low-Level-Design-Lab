from enum import Enum, auto


class BookCopyStatus(Enum):
    AVAILABLE = auto()
    BORROWED = auto()
    RESERVED = auto()


class LoanStatus(Enum):
    ACTIVE = auto()
    RETURNED = auto()


class ReservationStatus(Enum):
    WAITING = auto()
    READY = auto()
    COMPLETED = auto()
    CANCELLED = auto()
