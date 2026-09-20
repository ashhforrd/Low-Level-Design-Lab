from .player import Player
from .board import Board
from .winning_strategy import WinningStrategy
from .enums import GameState
from typing import Optional

class Game:
    def __init__(self, player_one: Player, player_two: Player, winning_strategy: WinningStrategy) -> None:
        if player_one.mark == player_two.mark:
            raise ValueError("Player must use different marks")

        self.board = Board()
        self.players: list[Player] = [player_one, player_two]
        self.current_player_index = 0
        self.state = GameState.IN_PROGRESS
        self.winner: Optional[Player] = None
        self.winning_strategy = winning_strategy

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    def make_move(self, row: int, column: int) -> None:
        if self.state != GameState.IN_PROGRESS:
            raise ValueError("Cannot make a move the game has ended")

        current_player = self.current_player

        self.board.place_mark(row, column, current_player.mark)

        if self.winning_strategy.is_winner(self.board, current_player.mark):
            self.state = GameState.WON
            self.winner = current_player
            return
        
        if self.board.is_full():
            self.state = GameState.DRAW
            return

        self.current_player_index = (self.current_player_index + 1) % len(self.players)