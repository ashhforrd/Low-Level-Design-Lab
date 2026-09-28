import time
import threading


class UnsafeSeatInventory:
    def __init__(self, capacity: int) -> None:
        self.available_seats = capacity

    def reserve(self) -> bool:
        if self.available_seats <= 0:
            return False

        current_seats = self.available_seats

        time.sleep(0.01)

        self.available_seats = current_seats - 1
        return True


class SeatInventory:
    def __init__(self, capacity: int) -> None:
        self.available_seats = capacity
        self.lock = threading.Lock()

    def reserve(self) -> bool:
        with self.lock:
            if self.available_seats <= 0:
                return False

            current_seats = self.available_seats

            time.sleep(0.01)

            self.available_seats = current_seats - 1
            return True


def run_unsafe_scenario() -> None:
    inventory = SeatInventory(capacity=5)

    worker_count = 10
    results = [False] * worker_count
    threads: list[threading.Thread] = []

    def reserve_seat(worker_index: int) -> None:
        results[worker_index] = inventory.reserve()

    for worker_index in range(worker_count):
        thread = threading.Thread(
            target=reserve_seat,
            args=(worker_index,),
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    successful_reservations = sum(results)

    print("Successful reservations: ", successful_reservations)
    print("Available seats: ", inventory.available_seats)


if __name__ == "__main__":
    run_unsafe_scenario()
