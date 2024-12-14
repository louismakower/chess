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

    def checkmate(self, player):
        if not self.board.in_check(player.colour):
            return False
        if len(player.all_moves()) > 0:
            return False
        return True

    def announce_loser(self):
        print(f'{self.current_player.colour} loses')

    def announce_move(self, move):
        printme = f'{self.current_player.colour.upper()} moved {move.piece.label} from {move.old} to {move.new}'
        print(printme)

    def play(self):
        while not self.checkmate(self.current_player):
            self.board.draw()
            self.announce_player()
            move = self.current_player.make_move()
            self.announce_move(move)
            self.switch_player()
        self.board.draw()
        self.announce_loser()


if __name__ == "__main__":
    game = Game()
    game.play()