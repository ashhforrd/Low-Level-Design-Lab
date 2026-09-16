from abc import ABC, abstractmethod


class Bird(ABC):
    @abstractmethod
    def move(self) -> str:
        pass


class FlyingBird(Bird):
    @abstractmethod
    def fly(self) -> str:
        pass


class Sparrow(FlyingBird):
    def move(self) -> str:
        return self.fly()

    def fly(self) -> str:
        return  "Sparrow is flying"


class Penguin(Bird):
    def move(self) -> str:
        return "Penguin is swimming"


def move_bird(bird: Bird) -> None:
    print(bird.move())


def start_flight(bird: FlyingBird) -> None:
    print(bird.fly())


if __name__ == "__main__":
    sparrow = Sparrow()
    penguin = Penguin()

    move_bird(sparrow)
    move_bird(penguin)

    start_flight(sparrow)