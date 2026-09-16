from abc import ABC, abstractmethod


class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass


class EmailNotification(Notification):
    def __init__(self, email_address: str):
        self.email_address = email_address

    def send(self, message: str) -> None:
        print(f"Sending email to {self.email_address}: {message}")



class SMSNotification(Notification):
    def __init__(self, phone_number: str):
        self.phone_number = phone_number

    def send(self, message: str) -> None:
        print(f"Sending SMS to {self.phone_number}: {message}")



if __name__ == "__main__":
    email = EmailNotification("budi@example.com")
    sms = SMSNotification("08123456789")

    email.send("Pesanan sedang dikirim")
    sms.send("Kode OTP: 123456")