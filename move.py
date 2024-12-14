class Move:
    def __init__(self, piece, old: tuple, new: tuple):
        self.piece = piece
        self.old = old
        self.new = new