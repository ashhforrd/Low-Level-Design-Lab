from abc import ABC, abstractmethod

from .enums import VehicleType


class Vehicle(ABC):
    def __init__(self, license_plate: str):
        normalized_plate = license_plate.strip().upper()

        if not normalized_plate:
            raise ValueError("License plate tidak boleh kosong")

        self._license_plate = normalized_plate

    @property
    def license_plate(self) -> str:
        return self._license_plate

    @property
    @abstractmethod
    def vehicle_type(self) -> VehicleType:
        pass


class Motorcycle(Vehicle):
    @property
    def vehicle_type(self) -> VehicleType:
        return VehicleType.MOTORCYCLE


class Car(Vehicle):
    @property
    def vehicle_type(self) -> VehicleType:
        return VehicleType.CAR


class BoxTruck(Vehicle):
    @property
    def vehicle_type(self) -> VehicleType:
        return VehicleType.BOX_TRUCK