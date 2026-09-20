from .enums import Mark

class Player:
    def __init__(self, name: str, mark: Mark) -> None:
        normalized_name = name.strip()

        if normalized_name == "":
            raise ValueError("Name cannot be empty")

        if not isinstance(mark, Mark):
            raise TypeError("Mark must be an instance of Mark")

        self.name = normalized_name
        self.mark = mark