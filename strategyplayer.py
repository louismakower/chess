import random
from player import Player
from pieces import Move

colour_scores = {'w':1, 'b':-1}

class AutomaticPlayer(Player):
    """ Automatic player using simple heuristic and alpha-beta pruning."""
    def __init__(self, colour, board, cutoff: int, rand: float=None, verbose=False):
        """
        Params:
            colour [str]: the colour of the pieces the player can move.  Should be 'b' or 'w'.
            board [Board]: the board
            cutoff [int]: how many moves ahead to search
            rand [float]: the player will act completely randomly with his probability per move
            """
        super().__init__(colour, board)
        self.cutoff = cutoff
        self.rand = rand
        self.prev_eval = 0
        self.verbose = verbose

    def make_move(self):
        if self.rand or self.cutoff == 0:
            if not self.rand:
                self.rand = 1
            # somtimes act randomly to spice things up a bit
            coin = random.random()
            if coin < self.rand or self.cutoff == 0:
                move = random.choice(self.board.get_colour_moves(self.colour))
                print('acted randomly')
                return move

        print('Thinking...')
        value, move = self.cut_off_ab_search(0)
        if self.verbose:
            print(f'previous {self.cutoff} moves ahead: {self.prev_eval}')
            print(f'now {self.cutoff} moves ahead: {value}')
            print(f'current board evaluation: {self.evaluation()}')
        self.prev_eval = value
        return move

    def get_pieces_new_board(self, board):
        return [piece for piece in board.get_pieces().values() if piece.colour == self.colour]

    def cutoff_test(self, depth):
        return depth >= self.cutoff

    def evaluation(self):
        total = 0
        # reward getting opponent in check
        if self.board.in_check('b'):
            total += 2
        if self.board.in_check('w'):
            total += -2

        white_legal_moves = len(self.board.get_colour_moves('w'))
        black_legal_moves = len(self.board.get_colour_moves('b'))
        total += (white_legal_moves - black_legal_moves) * 0.01 # reward having high mobility

        # aim for checkmate
        if self.board.result('b') == 'checkmate':
            total += 10000
        if self.board.result('w') == 'checkmate':
            total += -10000

        # avoid stalemate
        if self.colour == 'w' and self.board.result('b') == 'stalemate':
            total -= 1000
        if self.colour == 'b' and self.board.result('w') == 'stalemate':
            total += 1000

        for piece in self.board.get_pieces().values():
            sign = colour_scores[piece.colour]
            total += sign * piece.value
        return total

    def cut_off_ab_search(self, depth):
        alpha = float('-inf')
        beta = float('inf')

        if self.colour == 'w':
            best_action, best_value = self.max_value(alpha, beta, depth)
        else:
            best_action, best_value = self.min_value(alpha, beta, depth)

        return best_action, best_value

    def max_value(self, alpha, beta, depth) -> (float, Move):
        if self.cutoff_test(depth):
            return self.evaluation(), None

        v = float('-inf')
        best_action = None
        for move in self.board.get_colour_moves('w'):
            self.board.move_piece(move)
            min_v, _ = self.min_value(alpha, beta, depth+1)
            self.board.undo_move(move)
            if min_v > v:
                v = min_v
                best_action = move
            if v >= beta:
                return v, best_action
            alpha = max(alpha, v)
        return v, best_action

    def min_value(self, alpha, beta, depth) -> (float, Move):
        if self.cutoff_test(depth):
            return self.evaluation(), None

        v = float('inf')
        best_action = None
        for move in self.board.get_colour_moves('b'):
            self.board.move_piece(move)
            max_v, _ = self.max_value(alpha, beta, depth + 1)
            self.board.undo_move(move)
            if max_v < v:
                v = max_v
                best_action = move
            if v <= alpha:
                return v, best_action
            beta = min(beta, v)
        return v, best_action