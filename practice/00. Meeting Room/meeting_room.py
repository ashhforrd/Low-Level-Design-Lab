from enum import Enum, auto
from datetime import datetime
from uuid import uuid4

class BookingStatus(Enum):
    ACTIVE = auto()
    CANCELLED = auto()


class Room:
    def __init__(self, room_id: str) -> None:
        self.room_id = room_id


class Booking:
    def __init__(self, booking_id: str, user_id: str, room: Room, start_time: datetime, end_time: datetime) -> None:
        if start_time >= end_time:
            raise ValueError("start_time must be earlier than end_time")
        
        self.booking_id = booking_id
        self.user_id = user_id
        self.room = room
        self.start_time = start_time
        self.end_time = end_time
        self.status = BookingStatus.ACTIVE

    def cancel(self) -> None:
        if self.status == BookingStatus.CANCELLED:
            raise ValueError("Booking is already cancelled")
        
        self.status = BookingStatus.CANCELLED


class MeetingRoomSystem:
    def __init__(self) -> None:
        self.rooms: dict[str, Room] = {}
        self.bookings: dict[str, Booking] = {}

    def add_room(self, room: Room) -> None:
        if room.room_id in self.rooms:
            raise ValueError("Room already exists")
        
        self.rooms[room.room_id] = room

    def book_room(self, user_id: str, room_id: str, start_time: datetime, end_time: datetime) -> Booking:
        room = self.rooms.get(room_id)

        if room is None:
            raise ValueError("Room was not found")

        booking_id = str(uuid4())
        new_booking = Booking(booking_id, user_id, room, start_time, end_time)

        for booking in self.bookings.values():
            is_same_room = booking.room.room_id == room_id
            is_active = booking.status == BookingStatus.ACTIVE
            is_overlapping = (
                start_time < booking.end_time
                and end_time > booking.start_time
            )

            if is_same_room and is_active and is_overlapping:
                raise ValueError("Room is already booked for this time")

        self.bookings[booking_id] = new_booking
        return new_booking

    def cancel_booking(self, booking_id: str) -> None:
        booking = self.bookings.get(booking_id)

        if booking is None:
            raise ValueError("Booking doesn't exist")

        booking.cancel()

def main() -> None:
    system = MeetingRoomSystem()
    system.add_room(Room("ROOM-1"))

    first_booking = system.book_room(
        user_id="USER-1",
        room_id="ROOM-1",
        start_time=datetime(2026, 1, 1, 10, 0),
        end_time=datetime(2026, 1, 1, 11, 0),
    )
    print("First booking created:", first_booking.booking_id)

    try:
        system.book_room(
            user_id="USER-2",
            room_id="ROOM-1",
            start_time=datetime(2026, 1, 1, 10, 30),
            end_time=datetime(2026, 1, 1, 11, 30),
        )
    except ValueError as error:
        print("Overlapping booking rejected:", error)

    system.cancel_booking(first_booking.booking_id)
    print("First booking status:", first_booking.status)

    second_booking = system.book_room(
        user_id="USER-2",
        room_id="ROOM-1",
        start_time=datetime(2026, 1, 1, 10, 30),
        end_time=datetime(2026, 1, 1, 11, 30),
    )
    print("Second booking created:", second_booking.booking_id)


if __name__ == "__main__":
    main() 