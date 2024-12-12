class Piece:
    def __init__(self, colour: str):
        self.colour = colour

class Pawn(Piece):
    def __init__(self, colour: str):
        super().__init__(colour)

    def __str__(self):
        return f'{self.colour} P '

class Rook(Piece):
    def __init__(self, colour: str):
        super().__init__(colour)

    def __str__(self):
        return f'{self.colour} R '

class Bishop(Piece):
    def __init__(self, colour: str):
        super().__init__(colour)
    def __str__(self):
        return f'{self.colour} B '

class Knight(Piece):
    def __init__(self, colour: str):
        super().__init__(colour)
    def __str__(self):
        return f'{self.colour} Kn'

class King(Piece):
    def __init__(self, colour: str):
        super().__init__(colour)
    def __str__(self):
        return f'{self.colour} K '

class Queen(Piece):
    def __init__(self, colour: str):
        super().__init__(colour)
    def __str__(self):
        return f'{self.colour} Q '