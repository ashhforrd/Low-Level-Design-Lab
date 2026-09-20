from enum import Enum, auto


class Mark(Enum):
    X = auto()
    O = auto()


class GameState(Enum):
    IN_PROGRESS = auto()
    WON = auto()
    DRAW = auto()