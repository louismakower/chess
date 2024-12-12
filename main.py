from pieces import Pawn, Rook, Knight, Bishop, Queen, King
row_labels = {1:'A', 2:'B', 3:'C', 4:'D', 5:'E', 6:'F', 7:'G', 8:'H'}

class Square:
    def __init__(self, colour, row, col):
        self.colour = colour
        self.occupied = False
        self.location = (row, col)
        self.label = f'{row_labels[row]}{col}'

    def __str__(self):
        return str((self.location, self.label, self.occupied))

class Board:
    def __init__(self):
        self.squares = {}
        self.pieces = []

    def _make_board(self):
        colours = ['b', 'w']
        for row in range(1,9):
            for col in range(1,9):
                self.squares[f'{row_labels[row]}{col}'] = Square(colours[(row+col)%2], row, col)
                # (row+col)%2 ensures the colour switches in the correct way


    def __getitem__(self, coords):
        row = coords[0]
        col = coords[1]
        return self.squares[f'{row_labels[row]}{col}']

    def reset(self):
        self.squares, self.pieces = {}, []
        self._make_board()
        # add black pawns
        for col in range(1,9):
            curr_square = self.squares[f'{row_labels[7]}{col}']
            curr_square.occupied = True
            self.pieces.append(Pawn('b', curr_square))

        # add white pawns
        for col in range(1, 9):
            curr_square = self.squares[f'{row_labels[2]}{col}']
            curr_square.occupied = True
            self.pieces.append(Pawn('w', curr_square))

        # add other black pieces
        self.pieces.append(Rook('b', self.squares['A8']))
        self.squares['A8'].occupied = True

        self.pieces.append(Rook('b', self.squares['H8']))
        self.squares['H8'].occupied = True

        self.pieces.append(Knight('b', self.squares['B8']))
        self.squares['B8'].occupied = True

        self.pieces.append(Knight('b', self.squares['G8']))
        self.squares['G8'].occupied = True

        self.pieces.append(Bishop('b', self.squares['C8']))
        self.squares['C8'].occupied = True

        self.pieces.append(Bishop('b', self.squares['F8']))
        self.squares['F8'].occupied = True

        self.pieces.append(Queen('b', self.squares['D8']))
        self.squares['D8'].occupied = True

        self.pieces.append(King('b', self.squares['E8']))
        self.squares['E8'].occupied = True

        # add other white pieces
        self.pieces.append(Rook('w', self.squares['A8']))
        self.squares['A1'].occupied = True

        self.pieces.append(Rook('w', self.squares['H8']))
        self.squares['H1'].occupied = True

        self.pieces.append(Knight('w', self.squares['B8']))
        self.squares['B1'].occupied = True

        self.pieces.append(Knight('w', self.squares['G8']))
        self.squares['G1'].occupied = True

        self.pieces.append(Bishop('w', self.squares['C8']))
        self.squares['C1'].occupied = True

        self.pieces.append(Bishop('w', self.squares['F8']))
        self.squares['F1'].occupied = True

        self.pieces.append(Queen('w', self.squares['D8']))
        self.squares['D1'].occupied = True

        self.pieces.append(King('w', self.squares['E8']))
        self.squares['E1'].occupied = True



if __name__ == '__main__':
    board = Board()
    board.reset()
    print(board[1,1])