from typing import Optional

from .enums import SpotType, VehicleType
from .vehicle import Vehicle


class ParkingSpot:
    def __init__(self, spot_id: str, spot_type: SpotType):
        if not spot_id.strip():
            raise ValueError("Spot ID tidak boleh kosong")

        self._spot_id = spot_id
        self._spot_type = spot_type
        self._parked_vehicle: Optional[Vehicle] = None

    @property
    def spot_id(self) -> str:
        return self._spot_id

    @property
    def spot_type(self) -> str:
        return self._spot_type

    @property
    def parked_vehicle(self) -> Optional[Vehicle]:
        return self._parked_vehicle

    @property
    def is_available(self) -> bool:
        return self._parked_vehicle is None

    def can_fit(self, vehicle: Vehicle) -> bool:
        compatible_types = _COMPATIBLE_VEHICLES[self._spot_type]
        return vehicle.vehicle_type in compatible_types

    def park(self, vehicle: Vehicle) -> None:
        if not self.is_available:
            raise ValueError(f"Spot {self._spot_id} sudah terisi")

        if not self.can_fit(vehicle):
            raise ValueError(f"{vehicle.vehicle_type.name} tidak kompatibel "
                             f"dengan {self._spot_type.name}"
                             )

        self._parked_vehicle = vehicle

    def remove_vehicle(self) -> Vehicle:
        if self._parked_vehicle is None:
            raise ValueError(f"Spot {self._spot_id} sudah kosong")

        vehicle = self._parked_vehicle
        self._parked_vehicle = None

        return vehicle


_COMPATIBLE_VEHICLES = {
    SpotType.MOTORCYCLE: {
        VehicleType.MOTORCYCLE,
    },
    SpotType.COMPACT: {
        VehicleType.MOTORCYCLE,
        VehicleType.CAR,
    },
    SpotType.LARGE: {
        VehicleType.MOTORCYCLE,
        VehicleType.CAR,
        VehicleType.BOX_TRUCK,
    },
}