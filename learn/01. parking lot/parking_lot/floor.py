from typing import List, Optional

from .spot import ParkingSpot
from .vehicle import Vehicle


class ParkingFloor:
    def __init__(self, floor_id: str, spots: List[ParkingSpot]):
        if not floor_id.strip():
            raise ValueError("Floor ID tidak boleh kosong")

        self._floor_id = floor_id
        self._spots = list(spots)

    @property
    def floor_id(self) -> str:
        return self._floor_id

    def find_available_spot(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        for spot in self._spots:
            if spot.is_available and spot.can_fit(vehicle):
                return spot

        return None