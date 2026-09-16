from abc import ABC, abstractmethod


class TrafficLightState(ABC):
    @abstractmethod
    def next(self) -> "TrafficLightState":
        pass

    @abstractmethod
    def color(self) -> str:
        pass


class RedState(TrafficLightState):
    def next(self) -> TrafficLightState:
        return GreenState()

    def color(self) -> str:
        return "RED"


class GreenState(TrafficLightState):
    def next(self) -> TrafficLightState:
        return YellowState()

    def color(self) -> str:
        return "GREEN"


class YellowState(TrafficLightState):
    def next(self) -> TrafficLightState:
        return RedState()

    def color(self) -> str:
        return "YELLOW"


class TrafficLight:
    def __init__(self):
        self.state: TrafficLightState = RedState()

    def change(self) -> None:
        self.state = self.state.next()

    def show(self) -> None:
        print(self.state.color())


if __name__ == "__main__":
    traffic_light = TrafficLight()

    traffic_light.show()
    traffic_light.change()

    traffic_light.show()
    traffic_light.change()

    traffic_light.show()
    traffic_light.change()

    traffic_light.show()