from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from enum import Enum, auto
from typing import Optional


class CarType(Enum):
    ECONOMY = auto()
    SUV = auto()
    LUXURY = auto()


class ReservationStatus(Enum):
    RESERVED = auto()
    PICKED_UP = auto()
    RETURNED = auto()
    CANCELLED = auto()


@dataclass(frozen=True)
class Car:
    car_id: str
    car_type: CarType


class Reservation:
    def __init__(
            self, 
            reservation_id: str, 
            customer_id: str, 
            car: Car, 
            start_date: date, 
            end_date: date,
            ) -> None:
        if start_date >= end_date:
            raise ValueError("Start date must lower than end date")

        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.car = car
        self.start_date = start_date
        self.end_date = end_date
        self.status = ReservationStatus.RESERVED
        self.pickup_date: Optional[date] = None
        self.return_date: Optional[date] = None