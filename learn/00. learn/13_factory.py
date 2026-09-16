from abc import ABC, abstractmethod
from enum import Enum, auto


class NotificationChannel(Enum):
    EMAIL = auto()
    SMS = auto()


class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass


class EmailNotification(Notification):
    def send(self, message: str) -> None:
        print(f"Email: {message}")


class SMSNotification(Notification):
    def send(self, message: str) -> None:
        print(f"SMS: {message}")


class NotificationFactory:
    @staticmethod
    def create(
        channel: NotificationChannel,
    ) -> Notification:
        if channel == NotificationChannel.EMAIL:
            return EmailNotification()
        elif channel == NotificationChannel.SMS:
            return SMSNotification()

        raise ValueError(f"Unsupported notification channel: {channel}")


if __name__ == "__main__":
    email = NotificationFactory.create(
        NotificationChannel.EMAIL
    )
    sms = NotificationFactory.create(
        NotificationChannel.SMS
    )

    email.send("Pesanan telah dikirim")
    sms.send("Kode OTP: 123456")
