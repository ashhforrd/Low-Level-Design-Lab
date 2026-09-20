from abc import ABC, abstractmethod
from .board import Board
from .enums import Mark


class WinningStrategy(ABC):
    @abstractmethod
    def is_winner(self, board: Board, mark: Mark) -> bool:
        pass


class StandardWinningStrategy(WinningStrategy):
    def is_winner(self, board: Board, mark: Mark) -> bool:
        for i in range(board.size):
            row_is_winning = True

            for j in range(board.size):
                if board.get_cell(i, j) != mark:
                    row_is_winning =  False
                    break

            if row_is_winning:
                return True

        for j in range(board.size):
            col_is_winning = True

            for i in range(board.size):
                if board.get_cell(i, j) != mark:
                    col_is_winning =  False
                    break

            if col_is_winning:
                return True

        main_diagonal_is_winning = True

        for index in range(board.size):
            if board.get_cell(index, index) != mark:
                main_diagonal_is_winning = False
                break

        if main_diagonal_is_winning:
            return True


        opposite_diagonal_is_winning = True

        for index in range(board.size):
            column = board.size - 1 - index

            if board.get_cell(index, column) != mark:
                opposite_diagonal_is_winning = False
                break

        if opposite_diagonal_is_winning:
            return True


        return False