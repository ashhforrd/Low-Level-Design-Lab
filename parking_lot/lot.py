from datetime import datetime
from typing import Callable, Dict, List, Optional
from uuid import uuid4

from .floor import ParkingFloor
from .pricing import PricingStrategy
from .spot import ParkingSpot
from .ticket import Ticket
from .vehicle import Vehicle


class ParkingLot:
    def __init__(
            self,
            floors: List[ParkingFloor],
            pricing_strategy: PricingStrategy,
            clock: Callable[[], datetime] = datetime.now,
    ):
        self._floors = list(floors)
        self._pricing_strategy = pricing_strategy
        self._clock = clock

        self._active_tickets: Dict[str, Ticket] = {}
        self._active_license_plates: Dict[str, str] = {}

    def park(self, vehicle: Vehicle) -> Ticket:
        if vehicle.license_plate in self._active_license_plates:
            raise ValueError(f"Kendaraan {vehicle.license_plate} sudah parkir")

        spot = self._find_available_spot(vehicle)

        if spot is None:
            raise ValueError("Tidak ada parking spot yang kompatibel")

        spot.park(vehicle)

        ticket = Ticket(
            ticket_id=str(uuid4()),
            vehicle=vehicle,
            spot=spot,
            entry_time=self._clock()
        )

        self._active_tickets[ticket.ticket_id] = ticket
        self._active_license_plates[vehicle.license_plate] = (
            ticket.ticket_id
        )

        return ticket

    def unpark(self, ticket_id: str) -> int:
        ticket = self._active_tickets.get(ticket_id)

        if ticket is None:
            raise ValueError(f"Ticket {ticket_id} tidak ditemukan atau sudah ditutup")

        exit_time = self._clock()

        fee = self._pricing_strategy.calculate_fee(
            ticket,
            exit_time,
        )

        ticket.close(exit_time)
        ticket.spot.remove_vehicle()

        del self._active_tickets[ticket_id]
        del self._active_license_plates[
            ticket.vehicle.license_plate
        ]

        return fee

    def _find_available_spot(
            self,
            vehicle: Vehicle,
    ) -> Optional[ParkingSpot]:
        for floor in self._floors:
            spot = floor.find_available_spot(vehicle)

            if spot is not None:
                return spot

        return None