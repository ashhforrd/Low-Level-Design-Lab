from typing import Optional
from .enums import Mark


class Board:
    def __init__(self) -> None:
        self.size = 3
        self.cells: list[list[Optional[Mark]]] = [[None for j in range(self.size)] for i in range(self.size)]

    def place_mark(self, row: int, column: int, mark: Mark) -> None:
        if row not in range(self.size) or column not in range(self.size):
            raise ValueError("Coordinate out of board")

        if not isinstance(mark, Mark):
            raise TypeError("mark must be an instance of Mark")

        if self.cells[row][column] is not None:
            raise ValueError("Cell is already occupied")

        self.cells[row][column] = mark

    def is_full(self) -> bool:
        for i in range(self.size):
            for j in range(self.size):
                if self.cells[i][j] is None:
                    return False
                
        return True

    def get_cell(self, row: int, column: int) -> Optional[Mark]:
        if row not in range(self.size) or column not in range(self.size):
            raise ValueError("Coordinate out of board")

        return self.cells[row][column]