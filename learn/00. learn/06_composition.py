from abc import ABC, abstractmethod


class Engine(ABC):
    @abstractmethod
    def start(self) -> str:
        pass


class GasolineEngine(Engine):
    def start(self) -> str:
        return "Gasoline engine started"


class ElectricEngine(Engine):
    def start(self) -> str:
        return "Electric engine started silently"


class Car:
    def __init__(self, brand: str, engine: Engine):
        self.brand = brand
        self.engine = engine

    def start(self) -> str:
        engine_messsage = self.engine.start()
        return f"{self.brand}: {engine_messsage}"


if __name__ == "__main__":
    gasoline_car = Car(
        "Toyota",
        GasolineEngine(),
    )

    electric_car = Car(
        "Tesla",
        ElectricEngine(),
    )

    print(gasoline_car.start())
    print(electric_car.start())