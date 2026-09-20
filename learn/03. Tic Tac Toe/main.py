from tic_tac_toe.game import Game
from tic_tac_toe.player import Player
from tic_tac_toe.enums import Mark
from tic_tac_toe.winning_strategy import StandardWinningStrategy

def main():
    player_1 = Player("Alice", Mark.X)
    player_2 = Player("Bob", Mark.O)

    strategy = StandardWinningStrategy()
    game = Game(player_1, player_2, strategy)

    game.make_move(0, 0)
    game.make_move(1, 0)        
    game.make_move(0, 1)
    game.make_move(1, 1)
    game.make_move(0, 2)

    print(game.state)
    print(game.winner.name)

    game2 = Game(player_1, player_2, strategy)

    game2.make_move(0, 0)
    game2.make_move(0, 1)        
    game2.make_move(0, 2)
    game2.make_move(1, 1)
    game2.make_move(1, 0)
    game2.make_move(1, 2)
    game2.make_move(2, 1)
    game2.make_move(2, 0)
    game2.make_move(2, 2)

    print(game2.state)
    print(game2.winner)

    game3 = Game(player_1, player_2, strategy)

    game3.make_move(0, 0)

    try:
        game3.make_move(0, 0)
    except ValueError as error:
        print(error)

    print(game3.current_player.name)


if __name__ == "__main__":
    main()