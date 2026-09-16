from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, message: str) -> None:
        pass


class EmailSubscriber(Observer):
    def __init__(self, email_address: str):
        self.email_address = email_address

    def update(self, message: str) -> None:
        print(f"Email to {self.email_address}: {message}")


class SMSSubscriber(Observer):
    def __init__(self, phone_number: str):
        self.phone_number = phone_number

    def update(self, message: str) -> None:
        print(f"SMS to {self.phone_number}: {message}")


class EventPublisher:
    def __init__(self):
        self.observers: list[Observer] = []

    def subscribe(self, observer: Observer) -> None:
        if observer not in self.observers:
            self.observers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        if observer in self.observers:
            self.observers.remove(observer)

    def notify(self, message: str) -> None:
        for observer in self.observers:
            observer.update(message)


if __name__ == "__main__":
    publisher = EventPublisher()

    email = EmailSubscriber("budi@example.com")
    sms = SMSSubscriber("08123456789")

    publisher.subscribe(email)
    publisher.subscribe(sms)

    publisher.notify("Pesanan sedang dikirim")

    publisher.unsubscribe(sms)

    publisher.notify("Pesanan telah sampai")