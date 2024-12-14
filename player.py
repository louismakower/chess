from board import convert
from move import Move
import random

class Player:
    def __init__(self, colour, board):
        self.colour = colour
        self.board = board

    def all_moves(self):
        moves = []
        for piece in self.board.get_pieces(self.colour):
            for move in piece.valid_moves(self.board):
                moves.append(move)
        return moves

    def make_move(self):
        raise NotImplementedError

class ManualPlayer(Player):
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
                        valid_moves = [self.board[move.new].label for move in piece.valid_moves(self.board)]
                        print(e)
                        print(valid_moves)
                    except ValueError:
                        valid_end = True
                        valid_piece = False
                    except AssertionError as e:
                        print(e)

        move = Move(piece, piece.square.location, new_coordinates)
        self.board.move_piece(move)
        return move

    def ask_for_piece(self):
        piece_to_move = input("Enter the label of the piece to move: ")
        old_coordinates = convert(piece_to_move)
        try:
            piece = self.board.pieces[old_coordinates]
        except KeyError:
            raise KeyError("There is no piece in this square, or the square is outside the board")
        assert piece.colour == self.colour, "You can only move your own pieces"
        return piece

    def ask_for_location(self, piece):
        old_coordinates = piece.square.location
        move_to = input(f"[Enter np to pick a new piece]\nEnter the label of the location to move {old_coordinates} to: ")

        if move_to == 'np':
            print("Select a new piece...")
            raise ValueError
        new_coordinates = convert(move_to)
        if new_coordinates not in [move.new for move in piece.valid_moves(self.board)]:
            raise KeyError("Not a valid move")
        else:
            return new_coordinates

class RandomPlayer(Player):
    def __init__(self, colour, board):
        super().__init__(colour, board)
        self.pieces = [piece for piece in board.pieces.values() if piece.colour == self.colour]

    def select_random_piece(self):
        piece = random.choice(self.pieces)
        return piece

    def select_random_move(self, piece):
        move = random.choice(piece.valid_moves(self.board))
        return move

    def make_move(self):
        valid_piece = False
        while not valid_piece:
            piece = self.select_random_piece()
            if len(piece.valid_moves(self.board)) > 0:
                valid_piece = True
        move = self.select_random_move(piece)


        self.board.move_piece(move)
        return move

class AutomaticPlayer(Player):
    pass