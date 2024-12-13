from board import convert

class Player:
    def __init__(self, colour, board):
        self.colour = colour
        self.board = board

class ManualPlayer(Player):
    def __init__(self, colour, board):
        super().__init__(colour, board)

    def make_move(self):
        valid_start = False
        while not valid_start:
            piece_to_move = input("Enter the label of the piece to move: ")
            old_coordinates = convert(piece_to_move)
            try:
                piece = self.board.pieces[old_coordinates]
                assert piece.colour == self.colour
                valid_start = True
            except AssertionError:
                print("You can only moved your own pieces")
            except KeyError:
                print("There is no piece in this square, or the square is outside the board")

        valid_end = False
        while not valid_end:
            move_to = input(f"Enter the label of the location to move {old_coordinates} to: ")
            new_coordinates = convert(move_to)
            if new_coordinates not in piece.moves(self.board):
                print("Not a valid move")
            else:
                self.board.move_piece(old_coordinates, new_coordinates)


class AutomaticPlayer(Player):
    pass