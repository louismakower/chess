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

        curr_col = self.square.location[0]
        curr_row = self.square.location[1]

        d_rows = {'b': -1, 'w': +1}
        d_row = d_rows[self.colour]

        # maybe can move one square forward
        not_take_end_squares.append(board[curr_col, curr_row + d_row])

        # if square ahead is free, and is in row 2 then can move 2 forward
        if curr_row == 2 and not board[curr_col, curr_row + d_row].occupant:
            not_take_end_squares.append(board[curr_col, curr_row + 2*d_row])

        try:
            two_squares_ahead = board[curr_col, curr_row + 2 * d_row]
        except ValueError:
            # todo: implement turning into queen here
            pass

        # can take diagonally
        try:
            take_end_squares.append(board[curr_col + 1, curr_row + d_row])
        except ValueError:
            # outside the board
            pass

        try:
            take_end_squares.append(board[curr_col - 1, curr_row + d_row])
        except ValueError:
            pass

        for move in take_end_squares:
            if move.occupant.colour != self.colour:
                valid_moves.append((move, True))

        for move in not_take_end_squares:
            if not move.occupant:
                valid_moves.append((move, False))

        return valid_moves

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