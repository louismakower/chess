import random
from board import label_to_coordinates
from pieces import Move

class Player:
    def __init__(self, colour, board):
        assert colour in {'w', 'b'}
        self.colour = colour
        self.board = board

    def make_move(self):
        raise NotImplementedError

class HumanPlayer(Player):
    def __init__(self, colour, board):
        super().__init__(colour, board)

    def make_move(self):
        valid_piece = False
        valid_end = False
        while not (valid_piece and valid_end):
            valid_end = False
            try:
                piece = self.ask_for_piece()
                valid_piece = True
            except AssertionError as e:
                print(e)
            except KeyError as e:
                print(e)
            except ValueError as e:
                print(e)

            if valid_piece and len(piece.valid_moves(self.board)) == 0:
                print("This piece has no valid moves")
                valid_piece = False

            if valid_piece:
                while not valid_end:
                    try:
                        new_coordinates = self.ask_for_location(piece)
                        valid_end = True
                    except KeyError as e:
                        valid_moves = [self.board.squares[move.new].label for move in piece.valid_moves(self.board)]
                        print(e)
                        print(valid_moves)
                    except ValueError:
                        valid_end = True
                        valid_piece = False
                    except AssertionError as e:
                        print(e)
        if new_coordinates == 'castle':
            move = piece.castle(self.board)
        else:
            move = Move(piece, piece.location, new_coordinates)
        return move

    def ask_for_piece(self):
        piece_to_move = input("[Enter the rook's location if you want to castle]\nEnter the label of the piece to move: ")
        old_coordinates = label_to_coordinates(piece_to_move)
        try:
            piece = self.board.get_pieces()[old_coordinates]
        except KeyError:
            raise KeyError("There is no piece in this square, or the square is outside the board")
        assert piece.colour == self.colour, "You can only move your own pieces"
        return piece

    def ask_for_location(self, piece):
        old_coordinates = piece.location
        move_to = input(f"[Enter np to pick a new piece]\n[Enter 'castle' to castle]\nEnter the label of the location to move {old_coordinates} to: ")
        if move_to == 'np':
            print("Select a new piece...")
            raise ValueError
        if move_to == 'castle':
            if not any(move.castle for move in piece.valid_moves(self.board)):
                raise KeyError("Can't castle at the moment")
            else:
                return 'castle'
        new_coordinates = label_to_coordinates(move_to)
        if new_coordinates not in [move.new for move in piece.valid_moves(self.board)]:
            raise KeyError("Not a valid move")
        else:
            return new_coordinates

class RandomPlayer(Player):
    def __init__(self, colour, board):
        super().__init__(colour, board)

    def make_move(self):
        move = random.choice(self.board.get_colour_moves(self.colour))
        return move

