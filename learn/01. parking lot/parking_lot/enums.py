from enum import Enum, auto


class VehicleType(Enum):
    MOTORCYCLE = auto()
    CAR = auto()
    BOX_TRUCK = auto()


class SpotType(Enum):
    MOTORCYCLE = auto()
    COMPACT = auto()
    LARGE = auto()


class TicketStatus(Enum):
    ACTIVE = auto()
    CLOSED = auto()