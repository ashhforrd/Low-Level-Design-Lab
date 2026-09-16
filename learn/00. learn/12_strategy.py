from abc import ABC, abstractmethod


class ShippingStrategy(ABC):
    @abstractmethod
    def calculate_cost(self, order_total: int) -> int:
        pass


class StandardShipping(ShippingStrategy):
    def calculate_cost(self, order_total: int) -> int:
        return 10_000


class ExpressShipping(ShippingStrategy):
    def calculate_cost(self, order_total: int) -> int:
        return 25_000


class FreeShipping(ShippingStrategy):
    def calculate_cost(self, order_total: int) -> int:
        return 0


class Checkout:
    def __init__(self, shipping_strategy: ShippingStrategy):
        self.shipping_strategy = shipping_strategy

    def calculate_grand_total(self, order_total: int) -> int:
        return order_total + self.shipping_strategy.calculate_cost(order_total)


if __name__ == "__main__":
    standard_checkout = Checkout(StandardShipping())
    express_checkout = Checkout(ExpressShipping())
    free_checkout = Checkout(FreeShipping())

    print(standard_checkout.calculate_grand_total(100_000))
    print(express_checkout.calculate_grand_total(100_000))
    print(free_checkout.calculate_grand_total(100_000))