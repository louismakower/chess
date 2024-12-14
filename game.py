from board import Board, coordinates_to_label, other_player
from player import HumanPlayer, RandomPlayer
from strategyplayer import AutomaticPlayer

class Game:
    def __init__(self, human_colour, computer_cutoff):
        self.board = Board()
        self.board.reset()
        if human_colour == 'w':
            self.p_white = HumanPlayer('w', self.board)
            self.p_black = AutomaticPlayer('b', self.board, computer_cutoff)
        elif human_colour == 'b':
            self.p_white = AutomaticPlayer('w', self.board, computer_cutoff)
            self.p_black = HumanPlayer('b', self.board)
        self.board.players = {'b': self.p_black, 'w': self.p_white}
        self.current_player = self.p_white

    def announce_player(self):
        print(f"It's {self.current_player.colour.upper()}'s turn")

    def switch_player(self):
        if self.current_player == self.p_black:
            self.current_player = self.p_white
        else:
            self.current_player = self.p_black

    def announce_loser(self):
        print(f'{self.current_player.colour} loses')

    def announce_move(self, move):
        printme = f'{self.current_player.colour.upper()} moved their {move.piece.name} from {coordinates_to_label(move.old)} to {coordinates_to_label(move.new)}'
        if move.castle:
            printme = f'{self.current_player.colour.upper()} castled with their {move.piece.name} in {move.piece.location}'
        print(printme)

    def play(self):
        num_moves = 0
        while True:
            num_moves += 1
            self.board.draw()
            self.announce_player()
            move = self.current_player.make_move()
            self.board.move_piece(move)
            self.announce_move(move)
            if self.board.in_check(other_player[self.current_player.colour]):
                print('Check!')
            self.switch_player()
            result = self.board.result(self.current_player.colour)
            if result:
                break
            if num_moves > 100:
                print("Move limit reached")
                result = 'stalemate'
                break

        self.board.draw()
        if result == 'stalemate':
            print("Stalemate.")
            print(f"There were {num_moves // 2} moves by each player")
            return 'stalemate', float('inf')

        else:
            print("Checkmate!")
            self.announce_loser()
            print(f"There were {num_moves//2} moves by each player")
            return self.current_player.colour, num_moves//2

if __name__ == "__main__":
    w_wins = 0
    b_wins = 0
    games = []
    game = Game('w', 2)
    loser, num_moves_each_player = game.play()
    winner = 'w' if loser == 'b' else 'b'
    if winner == 'w':
        w_wins += 1
    elif winner == 'b':
        b_wins += 1
    games.append([winner, num_moves_each_player])
    print(f'white wins: {w_wins}\nblack wins: {b_wins}')
    print(games)