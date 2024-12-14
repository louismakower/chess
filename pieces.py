class Move:
    def __init__(self, piece, old: tuple, new: tuple, captured_piece=None, castle=None):
        self.piece = piece
        self.old = old
        self.new = new
        self.captured_piece = captured_piece
        self.is_first_move = not piece.moved
        self.castle = castle

class Piece:
    def __init__(self, colour: str, location):
        self.colour = colour
        self.location = location
        self.moved = False
        self.promoted_from = None

    def __eq__(self, other):
        if not isinstance(other, Piece):
            return False
        return (
            self.colour == other.colour and
            self.location == other.location and
            self.moved == other.moved and
            self.promoted_from == other.promoted_from and
            self.__class__ == other.__class__
        )

    def get_diagonal_moves(self, curr_col, curr_row, colour, board, moves=None):
        if moves is None:
            moves = []

        for dcol, drow in [(1,1), (-1,-1), (1,-1), (-1,1)]:  # top left bottom right and vice versa
            dpos = 1
            while True:
                test_location = (curr_col + dpos*dcol, curr_row + dpos*drow)

                if not board.in_board(test_location):
                    break

                if board.squares[test_location].occupant:
                    if board.squares[test_location].occupant.colour != colour:
                        moves.append(Move(self, self.location, test_location))
                    break
                else:
                    moves.append(Move(self, self.location, test_location))
                    dpos += 1

        return moves

    def get_horizontal_moves(self, curr_col, curr_row, colour, board, moves=None):
        if moves is None:
            moves = []
        for dcol, drow in [(1,0), (0,1), (-1,0), (0,-1)]:
            dpos = 1
            while True:
                test_location = (curr_col + dpos*dcol, curr_row + dpos*drow)
                if not board.in_board(test_location):
                    break
                # if there's a player there, can take it iff opposite colour
                if board.squares[test_location].occupant:
                    if board.squares[test_location].occupant.colour != colour:
                        moves.append(Move(self, self.location, test_location))
                    # otherwise can't take it
                    break
                # if free square, can move there and beyond
                else:
                    moves.append(Move(self, self.location, test_location))
                    dpos += 1  # increment in same direction
        return moves

    def possible_moves(self, board):
        raise NotImplementedError

    def valid_moves(self, board):
        moves = self.possible_moves(board)
        valid_moves = []
        for move in moves:
            if not board.would_be_check(move, self.colour):
                valid_moves.append(move)
        return valid_moves

class Pawn(Piece):
    def __init__(self, colour: str, location):
        super().__init__(colour, location)
        self.value = 1
        self.label = f'{colour} P '
        self.name = 'pawn'

    def __str__(self):
        return self.label

    def possible_moves(self, board):
        end_squares = []
        curr_col = self.location[0]
        curr_row = self.location[1]

        d_rows = {'b': -1, 'w': +1}
        d_row = d_rows[self.colour]

        # can go one square forward if not occupied
        if (board.in_board((curr_col, curr_row + d_row)) and
                not board.squares[curr_col, curr_row + d_row].occupant):
            end_squares.append(Move(self, self.location, (curr_col, curr_row + d_row)))

        # if both squares ahead free, and pawn's first move then can move 2 forward
        if (board.in_board((curr_col, curr_row + 2*d_row)) and not self.moved
                and not board.squares[curr_col, curr_row + d_row].occupant
                and not board.squares[curr_col, curr_row + 2*d_row].occupant):
            end_squares.append(Move(self, self.location, (curr_col, curr_row + 2*d_row)))

        # can take diagonally if other colour present there
        if (board.in_board((curr_col+1, curr_row + d_row)) and
                board.squares[curr_col+1, curr_row + d_row].occupant
                and board.squares[curr_col+1, curr_row + d_row].occupant.colour != self.colour):
            end_squares.append(Move(self, self.location, (curr_col+1, curr_row+d_row)))

        if (board.in_board((curr_col-1, curr_row + d_row)) and
                board.squares[curr_col-1, curr_row + d_row].occupant
                and board.squares[curr_col-1, curr_row + d_row].occupant.colour != self.colour):
            end_squares.append(Move(self, self.location, (curr_col-1, curr_row+d_row)))

        return end_squares

class Rook(Piece):
    def __init__(self, colour: str, location):
        super().__init__(colour, location)
        self.value = 5
        self.label = f'{colour} R '
        self.name = 'rook'

    def __str__(self):
        return self.label

    def possible_moves(self, board):
        curr_col = self.location[0]
        curr_row = self.location[1]

        moves = self.get_horizontal_moves(curr_col, curr_row, self.colour, board)
        castle_rooks = board.get_castle_rooks(self.colour)
        if self.location in castle_rooks:
            moves.append(self.castle(board))
        return moves

    def castle(self, board):
        castle_rooks = board.get_castle_rooks(self.colour)
        new_r = castle_rooks[self.location][0]
        new_k = castle_rooks[self.location][1]
        king = board.kings()[self.colour]
        k_move = Move(king, king.location, new_k)
        return Move(self, self.location, new_r, castle=k_move)

class Bishop(Piece):
    def __init__(self, colour: str, location):
        super().__init__(colour, location)
        self.value = 3
        self.label = f'{colour} B '
        self.name = 'bishop'

    def __str__(self):
        return self.label

    def possible_moves(self, board):
        curr_col = self.location[0]
        curr_row = self.location[1]

        end_squares = self.get_diagonal_moves(curr_col, curr_row, self.colour, board)
        return end_squares

class Knight(Piece):
    def __init__(self, colour: str, location):
        super().__init__(colour, location)
        self.value = 3
        self.label = f'{colour} Kn'
        self.name = 'knight'

    def __str__(self):
        return self.label

    def possible_moves(self, board):
        end_squares = []

        curr_col = self.location[0]
        curr_row = self.location[1]

        for dcol, drow in [(2,1), (2,-1), (-2, 1), (-2, -1), (1,2), (1,-2), (-1, 2), (-1, -2)]:
            test_location = curr_col + dcol, curr_row + drow

            if not board.in_board(test_location):
                continue

            if board.squares[test_location].occupant:
                if board.squares[test_location].occupant.colour != self.colour:
                    end_squares.append(Move(self, self.location, test_location))
            else:
                end_squares.append(Move(self, self.location, test_location))
        return end_squares

class King(Piece):
    def __init__(self, colour: str, location):
        super().__init__(colour, location)
        self.value = 0
        self.label = f'{colour} K '
        self.name = 'king'

    def __str__(self):
        return self.label

    def possible_moves(self, board):
        end_squares = []

        curr_col = self.location[0]
        curr_row = self.location[1]

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

            if board.squares[test_location].occupant:
                if board.squares[test_location].occupant.colour != self.colour:
                    end_squares.append(Move(self, self.location, test_location))
            else:
                end_squares.append(Move(self, self.location, test_location))
        return end_squares

class Queen(Piece):
    def __init__(self, colour: str, location):
        super().__init__(colour, location)
        self.value = 9
        self.label = f'{colour} Q '
        self.name = 'queen'

    def __str__(self):
        return self.label

    def possible_moves(self, board):
        curr_col = self.location[0]
        curr_row = self.location[1]

        end_squares = self.get_diagonal_moves(curr_col, curr_row, self.colour, board)
        end_squares = self.get_horizontal_moves(curr_col, curr_row, self.colour, board, end_squares)

        return end_squares