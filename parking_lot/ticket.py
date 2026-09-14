from datetime import datetime
from typing import Optional

from .enums import TicketStatus
from .spot import ParkingSpot
from .vehicle import Vehicle


class Ticket:
    def __init__(
            self,
            ticket_id: str,
            vehicle: Vehicle,
            spot: ParkingSpot,
            entry_time: datetime,
    ):
        self._ticket_id = ticket_id
        self._vehicle = vehicle
        self._spot = spot
        self._entry_time = entry_time
        self._exit_time: Optional[datetime] = None
        self._status = TicketStatus.ACTIVE

    @property
    def ticket_id(self) -> str:
        return self._ticket_id

    @property
    def vehicle(self) -> Vehicle:
        return self._vehicle

    @property
    def spot(self) -> ParkingSpot:
        return self._spot

    @property
    def entry_time(self) -> datetime:
        return self._entry_time

    @property
    def exit_time(self) -> Optional[datetime]:
        return self._exit_time

    @property
    def status(self) -> TicketStatus:
        return self._status

    def close(self, exit_time: datetime) -> None:
        if self._status == TicketStatus.CLOSED:
            raise ValueError("Ticket sudah ditutup")

        if exit_time < self._entry_time:
            raise ValueError("Waktu keluar tidak boleh sebelum waktu masuk")

        self._exit_time = exit_time
        self._status = TicketStatus.CLOSED