from enum import Enum, auto
from typing import Optional

class Direction(Enum):
    IDLE = auto()
    UP = auto()
    DOWN = auto()


class DoorState(Enum):
    OPEN = auto()
    CLOSED = auto()


class Elevator:
    def __init__(self, min_floor: int, max_floor: int) -> None:
        if min_floor >= max_floor:
            raise ValueError("min_floor must be lower than max_floor")

        if not min_floor <= 0 <= max_floor:
            raise ValueError("Floor zero must be within the elevator range")

        self.current_floor = 0
        self.min_floor = min_floor
        self.max_floor = max_floor
        self.direction = Direction.IDLE
        self.door_state = DoorState.CLOSED
        self.pending_requests: list[int] = []

    def request_floor(self, destination_floor: int) -> None:
        if not self.min_floor <= destination_floor <= self.max_floor:
            raise ValueError(f"Floor {destination_floor} must be within the elevator range")

        if destination_floor in self.pending_requests:
            return

        self.pending_requests.append(destination_floor)

    def process_next_request(self) -> Optional[int]:
        if not self.pending_requests:
            self.direction = Direction.IDLE
            return None

        destination_floor = self.pending_requests.pop(0)

        if self.door_state == DoorState.OPEN:
            self.door_state = DoorState.CLOSED

        if destination_floor > self.current_floor:
            self.direction = Direction.UP
        elif destination_floor < self.current_floor:
            self.direction = Direction.DOWN
        else:
            self.direction = Direction.IDLE

        self.current_floor = destination_floor

        self.direction = Direction.IDLE
        self.door_state = DoorState.OPEN

        return destination_floor