from pieces import Pawn, Rook, Knight, Bishop, Queen, King
col_labels = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H'}

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

    def make_board(self):
        colours = ['b', 'w']
        for row in range(1,9):
            for col in range(1,9):
                self.squares[f'{col_labels[col]}{row}'] = Square(colours[(row + col) % 2], col, row)
                # (row+col)%2 ensures the colour switches in the correct way

    def reset(self):
        self.squares, self.pieces = {}, {}
        self.make_board()

        # add pawns
        for col in range(1, 9):
            # black pawns
            curr_square = self.squares[f'{col_labels[col]}{7}']
            curr_piece = Pawn('b', curr_square)
            curr_square.occupant = curr_piece
            self.pieces[curr_square.label] = curr_piece

            # white pawns
            curr_square = self.squares[f'{col_labels[col]}{2}']
            curr_piece = Pawn('w', curr_square)
            curr_square.occupant = curr_piece
            self.pieces[curr_square.label] = curr_piece

        blacks = [Rook('b', self.squares['A8']), Knight('b', self.squares['B8']), Bishop('b', self.squares['C8']),
                  Queen('b', self.squares['D8']), King('b', self.squares['E8']),
                  Bishop('b', self.squares['F8']), Knight('b', self.squares['G8']), Rook('b', self.squares['H8'])]

        whites = [Rook('w', self.squares['A1']), Knight('w', self.squares['B1']), Bishop('w', self.squares['C1']),
                  Queen('w', self.squares['D1']), King('w', self.squares['E1']),
                  Bishop('w', self.squares['F1']), Knight('w', self.squares['G1']), Rook('w', self.squares['H1'])]

        for col, piece in enumerate(blacks, start=1):
            self.pieces[f'{col_labels[col]}{8}'] = piece
            self.squares[f'{col_labels[col]}{8}'].occupant = piece

        for col, piece in enumerate(whites, start=1):
            self.pieces[f'{col_labels[col]}{1}'] = piece
            self.squares[f'{col_labels[col]}{1}'].occupant = piece

    def __getitem__(self, coords):
        col = coords[0]
        row = coords[1]
        if col < 1 or col > 8 or row < 1 or row > 8:
            raise ValueError("outside board")
        return self.squares[f'{col_labels[col]}{row}']

    def draw_board(self):
        print_me = "     A    B    C    D    E    F    G    H\n"
        print_me += "   " + "_"*41 + '\n'
        for row in range(8,0,-1):
            print_me += str(row) + ' | '
            for col in range(1, 9):
                square = self[col, row]
                print_me += str(square) + ' '
            print_me += '| ' + str(row) + '\n'
        print_me += "   " + "_" * 41 + '\n'
        print_me += "     A    B    C    D    E    F    G    H\n"

        print(print_me)


if __name__ == '__main__':
    board = Board()
    board.reset()
    # print(board.pieces['A2'].valid_moves(board))
    board.draw_board()