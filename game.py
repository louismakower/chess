from board import Board
from player import ManualPlayer
class Game:
    def __init__(self):
        self.board = Board()
        self.board.reset()
        self.p_white = ManualPlayer('w', self.board)
        self.p_black = ManualPlayer('b', self.board)
        self.current_player = self.p_white

    def switch_player(self):
        if self.current_player == self.p_black:
            self.current_player = self.p_white
        else:
            self.current_player = self.p_black
        print(f"Now it's {self.current_player.colour.upper()}'s turn")

    def play(self):
        while not self.board.terminal():
            self.board.draw_board()
            self.current_player.make_move()
            self.switch_player()

if __name__ == "__main__":
    game = Game()
    game.play()