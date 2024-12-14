import copy
from move import Move



class Piece:
    def __init__(self, colour: str, square):
        self.colour = colour
        self.square = square
        self.moved = False

    def get_diagonal_moves(self, curr_col, curr_row, colour, board, end_squares=None):
        if end_squares is None:
            end_squares = []

        for direction in ['TLBR', 'TRBL']:  # top left bottom right and vice versa
            for sign in [1, -1]:
                d_pos = 1 * sign
                while True:
                    if direction == 'TLBR':
                        test_location = (curr_col - d_pos, curr_row + d_pos)
                    else:
                        test_location = (curr_col + d_pos, curr_row + d_pos)

                    if not board.in_board(test_location):
                        break

                    if board[test_location].occupant:
                        if board[test_location].occupant.colour != colour:
                            end_squares.append(Move(self, self.square.location, test_location))
                        break

                    else:
                        end_squares.append(Move(self, self.square.location, test_location))
                        d_pos += sign

        return end_squares

    def get_horizontal_moves(self, curr_col, curr_row, colour, board, end_squares=None):
        if end_squares is None:
            end_squares = []
        for direction in ['vert', 'horz']:
            for sign in [1, -1]:  # up/down or left/right
                d_pos = 1 * sign  # will start in this direction
                while True:
                    if direction == 'vert':
                        test_location = (curr_col, curr_row + d_pos)
                    else:
                        test_location = (curr_col + d_pos, curr_row)

                    if not board.in_board(test_location):
                        break

                    # if there's a player there, can take it iff opposite colour
                    if board[test_location].occupant:
                        if board[test_location].occupant.colour != colour:
                            end_squares.append(Move(self, self.square.location, test_location))
                        # otherwise can't take it
                        break

                    # if free square, can move there and beyond
                    else:
                        end_squares.append(Move(self, self.square.location, test_location))
                        d_pos += sign  # increment in same direction
        return end_squares

    def including_check_moves(self, board):
        raise NotImplementedError

    def valid_moves(self, board):
        moves = self.including_check_moves(board)
        valid_moves = []
        for move in moves:
            if not board.would_be_check(move, self.colour):
                valid_moves.append(move)
        return valid_moves

class Pawn(Piece):
    def __init__(self, colour: str, square):
        super().__init__(colour, square)
        self.value = 1
        self.label = f'{colour} P '

    def __str__(self):
        return self.label

    def including_check_moves(self, board):
        end_squares = []
        curr_col = self.square.location[0]
        curr_row = self.square.location[1]

        d_rows = {'b': -1, 'w': +1}
        d_row = d_rows[self.colour]

        # can go one square forward if not occupied
        if (board.in_board((curr_col, curr_row + d_row)) and
                not board[curr_col, curr_row + d_row].occupant):
            end_squares.append(Move(self, self.square.location, (curr_col, curr_row + d_row)))

        # if both squares ahead free, and pawn's first move then can move 2 forward
        if (board.in_board((curr_col, curr_row + 2*d_row)) and not self.moved
                and not board[curr_col, curr_row + d_row].occupant
                and not board[curr_col, curr_row + 2*d_row].occupant):
            end_squares.append(Move(self, self.square.location, (curr_col, curr_row + 2*d_row)))

        # can take diagonally if other colour present there
        if (board.in_board((curr_col+1, curr_row + d_row)) and
                board[curr_col+1, curr_row + d_row].occupant
                and board[curr_col+1, curr_row + d_row].occupant.colour != self.colour):
            end_squares.append(Move(self, self.square.location, (curr_col+1, curr_row+d_row)))

        if (board.in_board((curr_col-1, curr_row + d_row)) and
                board[curr_col-1, curr_row + d_row].occupant
                and board[curr_col-1, curr_row + d_row].occupant.colour != self.colour):
            end_squares.append(Move(self, self.square.location, (curr_col-1, curr_row+d_row)))

        return end_squares

class Rook(Piece):
    def __init__(self, colour: str, square):
        super().__init__(colour, square)
        self.value = 5
        self.label = f'{colour} R '

    def __str__(self):
        return self.label

    def including_check_moves(self, board):
        curr_col = self.square.location[0]
        curr_row = self.square.location[1]

        end_squares = self.get_horizontal_moves(curr_col, curr_row, self.colour, board)

        return end_squares

class Bishop(Piece):
    def __init__(self, colour: str, square):
        super().__init__(colour, square)
        self.value = 3
        self.label = f'{colour} B '

    def __str__(self):
        return self.label

    def including_check_moves(self, board):
        curr_col = self.square.location[0]
        curr_row = self.square.location[1]

        end_squares = self.get_diagonal_moves(curr_col, curr_row, self.colour, board)
        return end_squares

class Knight(Piece):
    def __init__(self, colour: str, square):
        super().__init__(colour, square)
        self.value = 3
        self.label = f'{colour} Kn'

    def __str__(self):
        return self.label

    def including_check_moves(self, board):
        end_squares = []

        curr_col = self.square.location[0]
        curr_row = self.square.location[1]

        for direction2 in ['vert', 'horz']: # direction to move 2 cells in
            for sign in [1, -1]: # left/right or up/down for 2 cell move
                for direction1 in [1, -1]: # left/right or up/down for 1 cell move
                    if direction2 == 'vert':
                        test_location = (curr_col + direction1, curr_row + 2*sign)
                    else:
                        test_location = (curr_col + 2*sign, curr_row + direction1)

                    if not board.in_board(test_location):
                        continue

                    if board[test_location].occupant:
                        if board[test_location].occupant.colour != self.colour:
                            end_squares.append(Move(self, self.square.location, test_location))

                    else:
                        end_squares.append(Move(self, self.square.location, test_location))

        return end_squares

class King(Piece):
    def __init__(self, colour: str, square):
        super().__init__(colour, square)
        self.value = 0
        self.label = f'{colour} K '

    def __str__(self):
        return self.label

    def including_check_moves(self, board):
        end_squares = []

        curr_col = self.square.location[0]
        curr_row = self.square.location[1]

        directions = [
            (0, 1), (0, -1),  # Vertical
            (1, 0), (-1, 0),  # Horizontal
            (1, 1), (-1, -1),  # Diagonal
            (1, -1), (-1, 1)  # Diagonal
        ]

        for dcol, drow in directions:
            test_location = (curr_col + dcol, curr_row + drow)

            if not board.in_board(test_location):
                continue

            if board[test_location].occupant:
                if board[test_location].occupant.colour != self.colour:
                    end_squares.append(Move(self, self.square.location, test_location))
            else:
                end_squares.append(Move(self, self.square.location, test_location))
        return end_squares

class Queen(Piece):
    def __init__(self, colour: str, square):
        super().__init__(colour, square)
        self.value = 9
        self.label = f'{colour} Q '

    def __str__(self):
        return self.label

    def including_check_moves(self, board):
        curr_col = self.square.location[0]
        curr_row = self.square.location[1]

        end_squares = self.get_diagonal_moves(curr_col, curr_row, self.colour, board)
        end_squares = self.get_horizontal_moves(curr_col, curr_row, self.colour, board, end_squares)

        return end_squares