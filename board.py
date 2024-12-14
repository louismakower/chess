import copy

from pieces import Pawn, Rook, Knight, Bishop, Queen, King
col_labels = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H'}
reversed_col_labels = {'A': 1, 'B': 2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8}
other_colour = {'b':'w', 'w':'b'}

def convert(label):
    error_message = "Must be in form LETTER-NUMBER"
    assert len(label) == 2, error_message

    try:
        col = reversed_col_labels[label[0].upper()]
    except KeyError:
        raise ValueError("Column not found")
    try:
        row = int(label[1])
    except Exception:
        raise ValueError("Row not found")
    return col, row


class Square:
    def __init__(self, colour, col, row):
        self.colour = colour
        self.occupant = False
        self.location = (col, row)
        self.label = f'{col_labels[col]}{row}'

    def __str__(self):
        if self.occupant:
            return str(self.occupant)
        else:
            return '    '

class Board:
    def __init__(self):
        self.squares = {}
        self.pieces = {}
        self.kings = {}

    def get_pieces(self, colour):
        colour_pieces = []
        for piece in self.pieces.values():
            if piece.colour == colour:
                colour_pieces.append(piece)
        return colour_pieces

    def make_board(self):
        colours = ['b', 'w']
        for row in range(1,9):
            for col in range(1,9):
                self.squares[(col, row)] = Square(colours[(col + row) % 2], col, row)
                # (row+col)%2 ensures the colour switches in the correct way

    def reset(self):
        self.squares, self.pieces = {}, {}
        self.make_board()

        # add pawns
        for col in range(1, 9):
            # black pawns
            curr_square = self[(col, 7)]
            curr_piece = Pawn('b', curr_square)
            curr_square.occupant = curr_piece
            self.pieces[curr_square.location] = curr_piece

            # white pawns
            curr_square = self[(col, 2)]
            curr_piece = Pawn('w', curr_square)
            curr_square.occupant = curr_piece
            self.pieces[curr_square.location] = curr_piece

        blacks = [Rook('b', self[(1,8)]), Knight('b', self[(2,8)]), Bishop('b', self[(3,8)]),
                  Queen('b', self[(4,8)]), King('b', self[(5,8)]),
                  Bishop('b', self[(6,8)]), Knight('b', self[(7,8)]), Rook('b', self[(8,8)])]

        whites = [Rook('w', self[(1,1)]), Knight('w', self[(2,1)]), Bishop('w', self[(3,1)]),
                  Queen('w', self[(4,1)]), King('w', self[(5,1)]),
                  Bishop('w', self[(6,1)]), Knight('w', self[(7,1)]), Rook('w', self[(8,1)])]

        for col, piece in enumerate(blacks, start=1):
            self.pieces[(col, 8)] = piece
            self[(col, 8)].occupant = piece
            if isinstance(piece, King):
                self.kings['b'] = piece

        for col, piece in enumerate(whites, start=1):
            self.pieces[(col, 1)] = piece
            self[col, 1].occupant = piece
            if isinstance(piece, King):
                self.kings['w'] = piece

    def __getitem__(self, coords):
        col = coords[0]
        row = coords[1]
        if col < 1 or col > 8 or row < 1 or row > 8:
            raise ValueError("outside board")
        return self.squares[(col, row)]

    @staticmethod
    def in_board(coords):
        col = coords[0]
        row = coords[1]
        if 1 <= col <= 8 and 1 <= row <= 8:
            return True
        else:
            return False

    def draw(self):
        print_me = "     A    B    C    D    E    F    G    H\n"
        print_me += "   " + "_"*41 + '\n'
        for row in range(8,0,-1):
            print_me += str(row) + ' | '
            for col in range(1, 9):
                square = self[col, row]
                print_me += str(square) + ' '
            print_me += '| ' + str(row) + '\n\n'
        print_me += "   " + "_" * 41 + '\n'
        print_me += "     A    B    C    D    E    F    G    H\n"

        print(print_me)

    def move_piece(self, move):
        old_location = move.old
        new_location = move.new
        piece = move.piece
        # move doesn't take anything
        if new_location not in self.pieces:
            self.pieces[new_location] = piece # put in new square
            self[new_location].occupant = piece
            self[old_location].occupant = False # remove from old square
            piece.moved = True
            piece.square = self[new_location]
            del self.pieces[old_location]
        # move does take something
        elif self.pieces[new_location].colour != piece.colour:
            del self.pieces[new_location]
            self.pieces[new_location] = piece
            self[new_location].occupant = piece
            self[old_location].occupant = False
            piece.moved = True
            piece.square = self[new_location]
            del self.pieces[old_location]
        else:
            raise ValueError("Tried to take a piece of your own colour")

    def would_be_check(self, move, colour):
        new_board = copy.deepcopy(self)
        new_move = copy.deepcopy(move)
        new_board.move_piece(new_move)
        check = new_board.in_check(colour)
        del new_board
        del new_move
        return check

    def in_check(self, colour):
        opponent_pieces = self.get_pieces(other_colour[colour])
        for piece in opponent_pieces:
            for move in piece.including_check_moves(self):
                if move.new == self.kings[colour].square.location:
                    return True
        return False

if __name__ == '__main__':
    board = Board()
    board.reset()
    board.draw()

    board2 = copy.deepcopy(board)
    print(board2.in_check('b'))