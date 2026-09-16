from abc import ABC, abstractmethod


class Beverage(ABC):
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def cost(self) -> int:
        pass


class Coffee(Beverage):
    def description(self) -> str:
        return "Coffee"

    def cost(self) -> int:
        return 15_000


class BeverageDecorator(Beverage, ABC):
    def __init__(self, beverage: Beverage):
        self.beverage = beverage


class MilkDecorator(BeverageDecorator):
    def description(self) -> str:
        return self.beverage.description() + ", Milk"

    def cost(self) -> int:
        return self.beverage.cost() + 5_000


class SugarDecorator(BeverageDecorator):
    def description(self) -> str:
        return self.beverage.description() + ", Sugar"

    def cost(self) -> int:
        return self.beverage.cost() + 2_000


if __name__ == "__main__":
    beverage = Coffee()
    beverage = MilkDecorator(beverage)
    beverage = SugarDecorator(beverage)

    print(beverage.description())
    print(beverage.cost())