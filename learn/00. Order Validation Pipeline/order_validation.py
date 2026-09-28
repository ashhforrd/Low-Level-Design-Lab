from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional


@dataclass
class OrderRequest:
    customer_id: str
    amount: int
    shipping_address: str


class ValidationHandler(ABC):
    def __init__(self) -> None:
        self.next_handler: Optional["ValidationHandler"] = None

    def set_next(self, handler: "ValidationHandler") -> "ValidationHandler":
        self.next_handler = handler
        return handler

    def handle(self, request: OrderRequest) -> None:
        self.validate(request)

        if self.next_handler is not None:
            self.next_handler.handle(request)

    @abstractmethod
    def validate(self, request: OrderRequest) -> None:
        pass


class AmountValidator(ValidationHandler):
    def validate(self, request: OrderRequest) -> None:
        if request.amount <= 0:
            raise ValueError("Order amount must be greater than zero")


class AddressValidator(ValidationHandler):
    def validate(self, requst: OrderRequest) -> None:
        if requst.shipping_address.strip() == "":
            raise ValueError("Shipping address cannot be empty")


class FraudValidator(ValidationHandler):
    def __init__(self, maximum_amount: int) -> None:
        super().__init__()
        self.maximum_amount = maximum_amount

    def validate(self, request: OrderRequest) -> None:
        if request.amount > self.maximum_amount:
            raise ValueError("Order requires manual fraud review")


class OrderValidadtionPipeline:
    def __init__(self, first_handler: ValidationHandler) -> None:
        self.first_handler = first_handler

    def validate(self, request: OrderRequest) -> None:
        self.first_handler.handle(request)


def build_validation_pipeline() -> OrderValidadtionPipeline:
    amount_validator = AmountValidator()
    address_validator = AddressValidator()
    fraud_validator = FraudValidator(
        maximum_amount=10_000_000
    )

    amount_validator.set_next(address_validator).set_next(fraud_validator)

    return OrderValidadtionPipeline(amount_validator)


def main() -> None:
    pipeline = build_validation_pipeline()

    requests = [
        OrderRequest(
            customer_id="CUSTOMER-1",
            amount=500_000,
            shipping_address="Jakarta",
        ),
        OrderRequest(
            customer_id="CUSTOMER-2",
            amount=-10_000,
            shipping_address="Bandung",
        ),
        OrderRequest(
            customer_id="CUSTOMER-3",
            amount=200_000,
            shipping_address="   ",
        ),
        OrderRequest(
            customer_id="CUSTOMER-4",
            amount=20_000_000,
            shipping_address="Surabaya",
        ),
    ]

    for request in requests:
        try:
            pipeline.validate(request)
            print(
                request.customer_id,
                "VALID",
            )
        except ValueError as error:
            print(
                request.customer_id,
                "REJECTED:",
                error,
            )


if __name__ == "__main__":
    main()