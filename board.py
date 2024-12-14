import copy
from pieces import Pawn, Rook, Knight, Bishop, Queen, King, Move

col_labels = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H'}
reversed_col_labels = {'A': 1, 'B': 2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8}
other_player = {'b': 'w', 'w': 'b'}

def label_to_coordinates(label):
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

def coordinates_to_label(coordinates):
    col, row = coordinates
    col = col_labels[col]
    return str(col)+str(row)

class Square:
    def __init__(self, colour, col, row):
        self.colour = colour
        self.occupant = None
        self.location = (col, row)
        self.label = f'{col_labels[col]}{row}'

    def __str__(self):
        if self.occupant:
            return str(self.occupant)
        else:
            return '    '

    def __eq__(self, other):
        if not isinstance(other, Square):
            return False
        return (self.colour == other.colour and
                self.occupant == other.occupant and
                self.location == other.location)

class Board:
    def __init__(self):
        self.squares = {}

    def __eq__(self, other):
        if not isinstance(other, Board):
            return False

        # Compare all squares
        for location, square in self.squares.items():
            other_square = other.squares.get(location)
            if other_square is None or square != other_square:
                return False

        return True

    def get_pieces(self):
        return {square.location: square.occupant for square in self.squares.values() if square.occupant}

    def kings(self):
        kings = {}
        for piece in self.get_pieces().values():
            if isinstance(piece, King):
                kings[piece.colour] = piece
        return kings

    def get_coloured_pieces(self, colour):
        return [piece for piece in self.get_pieces().values() if piece.colour == colour]

    def make_board(self):
        colours = ['b', 'w']
        for row in range(1,9):
            for col in range(1,9):
                self.squares[(col, row)] = Square(colours[(col + row) % 2], col, row)
                # (row+col)%2 ensures the colour switches in the correct way

    def reset(self):
        self.squares = {}
        self.make_board()

        # add pawns
        for col in range(1, 9):
            # black pawns
            curr_square = self.squares[(col, 7)]
            curr_piece = Pawn('b', curr_square.location)
            curr_square.occupant = curr_piece

            # white pawns
            curr_square = self.squares[(col, 2)]
            curr_piece = Pawn('w', curr_square.location)
            curr_square.occupant = curr_piece

        blacks = [Rook('b', (1,8)), Knight('b', (2,8)), Bishop('b', (3,8)),
                  Queen('b',(4,8)), King('b', (5,8)),
                  Bishop('b', (6,8)), Knight('b', (7,8)), Rook('b', (8,8))]

        whites = [Rook('w', (1,1)), Knight('w', (2,1)), Bishop('w', (3,1)),
                  Queen('w', (4,1)), King('w', (5,1)),
                  Bishop('w', (6,1)), Knight('w', (7,1)), Rook('w', (8,1))]

        for col, piece in enumerate(blacks, start=1):
            self.squares[(col, 8)].occupant = piece

        for col, piece in enumerate(whites, start=1):
            self.squares[(col, 1)].occupant = piece

    @staticmethod
    def in_board(coords):
        col = coords[0]
        row = coords[1]
        if 1 <= col <= 8 and 1 <= row <= 8:
            return True
        else:
            return False

    def draw(self):
        print_me = "      A     B     C     D     E     F     G     H\n"
        print_me += "   " + "_"*41 + '\n'
        for row in range(8,0,-1):
            print_me += str(row) + ' || '
            for col in range(1, 9):
                square = self.squares[col, row]
                print_me += str(square) + ' |'
            print_me += '| ' + str(row) + '\n\n'
        print_me += "   " + "_" * 41 + '\n'
        print_me += "      A     B     C     D     E     F     G     H\n"

        print(print_me)

    def update_board_in_move(self, move):
        piece = move.piece

        # Record the captured piece
        move.captured_piece = self.squares[move.new].occupant

        # update the board
        self.squares[move.new].occupant = piece # put in new square
        self.squares[move.old].occupant = None  # remove from old square

        # update the piece
        piece.location = move.new
        piece.moved = True

        # check promotion
        self.promotion(piece)

    def move_piece(self, move: Move):
        if move.castle:
            self.move_piece(move.castle)
        # move doesn't take anything
        if move.new not in self.get_pieces():
            self.update_board_in_move(move)

        # move does take something
        elif self.get_pieces()[move.new].colour != move.piece.colour:
            self.update_board_in_move(move)
        else:
            raise TypeError("Tried to take a piece of your own colour")

    def undo_move(self, move: Move):
        """
        Undo a move on the board, restoring the board and piece states to before the move.
        """
        if move.castle:
            self.undo_move(move.castle)
        # Retrieve the piece involved in the move
        piece = move.piece

        # Revert the piece's location and moved status
        self.squares[move.old].occupant = piece
        self.squares[move.new].occupant = move.captured_piece  # Restore captured piece, if any
        piece.location = move.old

        # Reset the moved flag if the move was the piece's first move
        if move.is_first_move:
            piece.moved = False

        if move.piece.promoted_from:
            # Revert to the original pawn
            self.squares[move.old].occupant = move.piece.promoted_from
            move.piece.promoted_from = None  # Clear the reference to avoid reusing it
        else:
            self.squares[move.old].occupant = piece

    def would_be_check(self, move, colour):
        self.move_piece(move)
        check = self.in_check(colour)
        self.undo_move(move)
        return check

    def in_check(self, k_colour):
        k_col, k_row = self.kings()[k_colour].location

        # check by pawn
        pawn_direction = -1 if k_colour == 'b' else 1
        for dcol, drow in [(1, pawn_direction), (-1, pawn_direction)]:
            test_location = k_col + dcol, k_row + drow
            if not self.in_board(test_location):
                continue
            occupant = self.squares[test_location].occupant
            if occupant:
                if occupant.colour != k_colour and isinstance(occupant, Pawn):
                    return True

        # check by rook or queen
        for dcol, drow in [(1,0), (-1,0), (0,1), (0,-1)]:
            dpos = 1
            while True:
                test_location = k_col + dpos*dcol, k_row + dpos*drow
                if not self.in_board(test_location):
                    break
                occupant = self.squares[test_location].occupant
                if occupant:
                    if occupant.colour != k_colour and (isinstance(occupant, Rook)
                                                        or isinstance(occupant, Queen)):
                        return True
                    break
                dpos += 1

        # check by rook or queen
        for dcol, drow in [(1, 1), (-1, -1), (-1, 1), (1, -1)]:
            dpos = 1
            while True:
                test_location = k_col + dpos * dcol, k_row + dpos * drow
                if not self.in_board(test_location):
                    break
                occupant = self.squares[test_location].occupant
                if occupant:
                    if occupant.colour != k_colour and (isinstance(occupant, Bishop)
                                                        or isinstance(occupant, Queen)):
                        return True
                    break
                dpos += 1

        # check by knight
        for dcol, drow in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            test_location = k_col + dcol, k_row + drow
            if not self.in_board(test_location):
                continue
            occupant = self.squares[test_location].occupant
            if occupant:
                if occupant.colour != k_colour and isinstance(occupant, Knight):
                    return True

        # next to other king
        for dcol, drow in [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            test_location = k_col + dcol, k_row + drow
            if not self.in_board(test_location):
                continue
            occupant = self.squares[test_location].occupant
            if occupant:
                if occupant.colour != k_colour and isinstance(occupant, King):
                    return True
        return False

    def promotion(self, piece):
        if isinstance(piece, Pawn) and piece.promoted_from is None:
            if (piece.colour == 'w' and piece.location[1] == 8) or (piece.colour == 'b' and piece.location[1] == 1):
                new_queen = Queen(piece.colour, piece.location)
                new_queen.promoted_from = piece
                self.squares[new_queen.location].occupant = new_queen
                piece.promoted_from = None  # Ensure this is only set for promoted pawns

    def get_castle_rooks(self, colour):
        castle_rooks = {}
        king = self.kings()[colour]

        if king.moved:
            # can't castle if king already been moved
            return {}

        if self.in_check(colour):
            # can't castle out of check
            return {}

        rooks = [piece for piece in self.get_coloured_pieces(colour) if isinstance(piece, Rook) and piece.colour == colour]
        k_col, row = king.location

        for rook in rooks:
            if rook.moved:
                # can't castle if rook already been mved
                continue
            castle = True
            col = rook.location[0]
            d_col = 1 if k_col > col else -1
            col += d_col
            while col != k_col:
                if self.squares[(col, row)].occupant:
                    castle = False
                    break
                col += d_col
            if castle:
                new_rook_col = k_col - d_col
                new_k_col = k_col - 2*d_col
                castle_rooks[rook.location] = [(new_rook_col, row), (new_k_col, row)]
        return castle_rooks

    def get_colour_moves(self, colour):
        moves = []
        for piece in self.get_coloured_pieces(colour):
            for move in piece.valid_moves(self):
                moves.append(move)
        return moves

    def result(self, colour):
        if len(self.get_colour_moves(colour)) == 0:
            if self.in_check(colour):
                return 'checkmate'
            else:
                return 'stalemate'
        if len(self.get_pieces()) == 2:
            return 'stalemate'
        return False

if __name__ == '__main__':
    board = Board()
    board.reset()
    board.draw()
    board2 = copy.deepcopy(board)

    move = Move(board.get_pieces()[(2, 8)], (2, 8), (2, 6))
    board.move_piece(move)
    move2 = Move(board.get_pieces()[(3, 8)], (3, 8), (3, 6))
    board.move_piece(move2)
    move3 = Move(board.get_pieces()[(4, 8)], (4, 8), (4, 6))
    board.move_piece(move3)

    move = Move(board.get_pieces()[(6, 8)], (6, 8), (6, 6))
    board.move_piece(move)
    move2 = Move(board.get_pieces()[(7, 8)], (7, 8), (7, 6))
    board.move_piece(move2)
    board.draw()
    print(board.get_castle_rooks('b'))
