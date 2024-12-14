from board import Board
from player import ManualPlayer, RandomPlayer
class Game:
    def __init__(self):
        self.board = Board()
        self.board.reset()
        self.p_white = ManualPlayer('w', self.board)
        self.p_black = RandomPlayer('b', self.board)
        self.current_player = self.p_white

    def announce_player(self):
        print(f"It's {self.current_player.colour.upper()}'s turn")

    def switch_player(self):
        if self.current_player == self.p_black:
            self.current_player = self.p_white
        else:
            self.current_player = self.p_black

    def announce_winner(self, colour):
        print(f'{colour.upper()} wins')

    def play(self):
        while not self.board.terminal()[0]:
            self.board.draw()
            self.announce_player()
            self.current_player.make_move()
            self.switch_player()
            if self.board.terminal()[0]:
                winner = self.board.terminal()[1]
                break
        self.announce_winner(winner)


if __name__ == "__main__":
    game = Game()
    game.play()