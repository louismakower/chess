class Piece:
    def __init__(self, colour: str, square):
        self.colour = colour
        self.square = square

    def valid_moves(self, board):
        raise NotImplementedError

class Pawn(Piece):
    def __init__(self, colour: str, square):
        super().__init__(colour, square)

    def __str__(self):
        return f'{self.colour} P '

    def valid_moves(self, board):
        not_take_end_squares = []
        take_end_squares = []
        valid_moves = []

        curr_row = self.square.location[0]
        curr_col = self.square.location[1]

        if self.colour == 'w':
            if curr_row == 2:
                not_take_end_squares.append(board[curr_col, curr_row + 2])
                not_take_end_squares.append(board[curr_col, curr_row + 1])
            else:
                not_take_end_squares.append(board[curr_col, curr_row + 1])

            take_end_squares.append(board[curr_col + 1, curr_row + 1])
            take_end_squares.append(board[curr_col - 1, curr_row + 1])

        for move in take_end_squares:
            if move.occupied:
                valid_moves.append((move, True))

        for move in not_take_end_squares:
            if not move.occupied:
                valid_moves.

class Rook(Piece):
    def __init__(self, colour: str, square):
        super().__init__(colour, square)

    def __str__(self):
        return f'{self.colour} R '

class Bishop(Piece):
    def __init__(self, colour: str, square):
        super().__init__(colour, square)
    def __str__(self):
        return f'{self.colour} B '

class Knight(Piece):
    def __init__(self, colour: str, square):
        super().__init__(colour, square)
    def __str__(self):
        return f'{self.colour} Kn'

class King(Piece):
    def __init__(self, colour: str, square):
        super().__init__(colour, square)
    def __str__(self):
        return f'{self.colour} K '

class Queen(Piece):
    def __init__(self, colour: str, square):
        super().__init__(colour, square)
    def __str__(self):
        return f'{self.colour} Q '