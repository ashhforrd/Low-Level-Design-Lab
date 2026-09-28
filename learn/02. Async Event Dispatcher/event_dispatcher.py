from abc import ABC, abstractmethod
from dataclasses import dataclass

import threading

from queue import Queue
from typing import Optional


@dataclass
class Event:
    event_type: str
    message: str


class EventSubscriber(ABC):
    @abstractmethod
    def handle(self, event: Event) -> None:
        pass


class LoggingSubscriber(EventSubscriber):
    def handle(self, event: Event) -> None:
        print(
            f"[LOG] {event.event_type}: {event.message}"
        )


class EmailSubscriber(EventSubscriber):
    def __init__(self, email_address: str) -> None:
        self.email_address = email_address

    def handle(self, event: Event) -> None:
        print(
            f"[EMAIL to {self.email_address}] "
            f"{event.event_type}: {event.message}"
        )


class AsyncEventDispatcher:
    def __init__(self) -> None:
        self.subscribers: dict[str, list[EventSubscriber]] = {}
        self.event_queue: Queue[Optional[Event]] = Queue()
        self.worker: Optional[threading.Thread] = None

    def subscribe(self, event_type: str, subscriber: EventSubscriber) -> None:
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []

        self.subscribers[event_type].append(subscriber)

    def publish(self, event: Event) -> None:
        if self.worker is None or not self.worker.is_alive():
            raise ValueError("Dispatcher is not running")

        self.event_queue.put(event)

    def start(self) -> None:
        if self.worker is not None and self.worker.is_alive():
            raise ValueError("Dispatcher is already running")

        self.worker = threading.Thread(
            target=self.process_events,
        )
        self.worker.start()

    def process_events(self) -> None:
        while True:
            event = self.event_queue.get()

            try:
                if event is None:
                    return

                subscribers = self.subscribers.get(
                    event.event_type,
                    [],
                )

                for subscriber in subscribers:
                    try:
                        subscriber.handle(event)
                    except Exception as error:
                        print(
                            "Subscriber failed:",
                            error,
                        )
            finally:
                self.event_queue.task_done()

    def stop(self) -> None:
        if self.worker is None or not self.worker.is_alive():
            return

        # Sentinel diletakkan setelah seluruh event sebelumnya.
        self.event_queue.put(None)

        # Tunggu worker memproses event dan sentinel.
        self.worker.join()

        self.worker = None

def main() -> None:
    dispatcher = AsyncEventDispatcher()

    logging_subscriber = LoggingSubscriber()
    email_subscriber = EmailSubscriber(
        "customer@example.com"
    )

    dispatcher.subscribe(
        "ORDER_CREATED",
        logging_subscriber,
    )
    dispatcher.subscribe(
        "ORDER_CREATED",
        email_subscriber,
    )
    dispatcher.subscribe(
        "ORDER_SHIPPED",
        logging_subscriber,
    )
    dispatcher.subscribe(
        "ORDER_SHIPPED",
        email_subscriber,
    )

    dispatcher.start()

    dispatcher.publish(
        Event(
            event_type="ORDER_CREATED",
            message="Order ORD-1 has been created",
        )
    )

    dispatcher.publish(
        Event(
            event_type="ORDER_SHIPPED",
            message="Order ORD-1 has been shipped",
        )
    )

    dispatcher.stop()

    print("Dispatcher stopped")


if __name__ == "__main__":
    main()