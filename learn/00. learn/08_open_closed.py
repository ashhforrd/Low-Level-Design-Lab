from abc import ABC, abstractmethod


class DiscountPolicy(ABC):
    @abstractmethod
    def calculate_discount(self, total: int) -> int:
        pass


class NoDiscount(DiscountPolicy):
    def calculate_discount(self, total: int) -> int:
        return 0


class PercentageDicount(DiscountPolicy):
    def __init__(self, percentage: int):
        if percentage < 0 or percentage > 100:
            raise ValueError("Percentage harus antara 0 dan 100")

        self.percentage = percentage

    def calculate_discount(self, total: int) -> int:
        return total * self.percentage // 100


class Checkout:
    def __init___(self, discount_policy: DiscountPolicy):
        self.discount_policy = discount_policy

    def calculate_final_price(self, total: int) -> int:
        discount = self.discount_policy.calculate_discount(total)

        return total - discount


if __name__ == "__main__":
    normal_checkout = Checkout(NoDiscount())
    member_checkout = Checkout(PercentageDicount(10))

    print(normal_checkout.calculate_final_price(100_000))
    print(member_checkout.calculate_final_price(100_000))