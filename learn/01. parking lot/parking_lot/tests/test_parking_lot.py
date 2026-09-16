import unittest
from datetime import datetime, timedelta

from parking_lot.enums import SpotType, TicketStatus
from parking_lot.floor import ParkingFloor
from parking_lot.lot import ParkingLot
from parking_lot.pricing import HourlyPricingStrategy
from parking_lot.spot import ParkingSpot
from parking_lot.vehicle import BoxTruck, Car


class ParkingLotTest(unittest.TestCase):
    def test_park_and_unpark_vehicle(self):
        # Arrange
        entered = datetime(2026, 9, 15, 10, 0)
        exited = entered + timedelta(minutes=61)

        times = iter([entered, exited])
        clock = lambda: next(times)

        spot = ParkingSpot("F1-C1", SpotType.COMPACT)
        floor = ParkingFloor("F1", [spot])

        lot = ParkingLot(
            floors=[floor],
            pricing_strategy=HourlyPricingStrategy(5000),
            clock=clock,
        )

        car = Car("B 1 CAR")

        # Act
        ticket = lot.park(car)
        fee = lot.unpark(ticket.ticket_id)

        # Assert
        self.assertEqual(fee, 10000)
        self.assertEqual(ticket.status, TicketStatus.CLOSED)
        self.assertTrue(spot.is_available)

    def test_same_vehicle_cannot_park_twice(self):
        # Arrange
        spot_one = ParkingSpot("C1", SpotType.COMPACT)
        spot_two = ParkingSpot("C2", SpotType.COMPACT)
        floor = ParkingFloor("F1", [spot_one, spot_two])

        lot = ParkingLot(
            floors=[floor],
            pricing_strategy=HourlyPricingStrategy(5000),
        )

        first_car = Car("B 1 CAR")
        same_car = Car("  b 1 car  ")

        # Act
        lot.park(first_car)

        # Assert
        with self.assertRaises(ValueError):
            lot.park(same_car)

    def test_rejects_vehicle_when_no_compatible_spot_exists(self):
        # Arrange
        compact_spot = ParkingSpot("C1", SpotType.COMPACT)
        floor = ParkingFloor("F1", [compact_spot])

        lot = ParkingLot(
            floors=[floor],
            pricing_strategy=HourlyPricingStrategy(5000),
        )

        truck = BoxTruck("B 2 TRUCK")

        # Act dan Assert
        with self.assertRaisesRegex(
            ValueError,
            "Tidak ada parking spot yang kompatibel",
        ):
            lot.park(truck)


if __name__ == "__main__":
    unittest.main()
