from abc import ABC, abstractmethod
from datetime import datetime
from math import ceil

from .ticket import Ticket


class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(
        self,
        ticket: Ticket,
        exit_time: datetime,
    ) -> int:
        pass


class HourlyPricingStrategy(PricingStrategy):
    def __init__(self, hourly_rate):
        if hourly_rate < 0:
            raise ValueError("TTarif tidak boleh negatif")

        self._hourly_rate = hourly_rate

    def calculate_fee(
        self, 
        ticket: Ticket, 
        exit_time: datetime
    ) -> int:
        if exit_time < ticket.entry_time:
            raise ValueError(
                "Waktuu keluar tidak boleh sebelum waktu masuuk"
            )

        duration = exit_time - ticket.entry_time
        total_seconds = duration.total_seconds()

        charges_hours = max(
            1,
            ceil(total_seconds / 3600),
        )

        return charges_hours * self._hourly_rate
        
        