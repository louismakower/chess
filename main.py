from pieces import Pawn, Rook, Knight, Bishop, Queen, King

class Square:
    def __init__(self, colour, row, column, piece=False):
        self.colour = colour
        self.piece = False
        self.row = row
        self.column = column

    def __str__(self):
        if self.piece:
            return str(self.piece)
        else:
            return '    '

class Board:
    def __init__(self):
        self.board = []
        for i in range(4):
            self.board.append(self.new_row('w', 8-2*i))
            self.board.append(self.new_row('b', 8-2*i-1))
        self.lookup_table = self._create_lookup_table()

    @staticmethod
    def new_row(initial_colour, column_num):
        row = []
        if initial_colour == 'w':
            for i in range(4):
                row.append(Square('w', 2*i+1, column_num))
                row.append(Square('b', 2*i+2, column_num))
        elif initial_colour == 'b':
            for i in range(4):
                row.append(Square('b', 2*i+1, column_num))
                row.append(Square('w', 2*i+2, column_num))
        else:
            raise ValueError("Colour provided not white or black")
        return row

    def _create_lookup_table(self):
        row_letters = {1:'A', 2:'B', 3:'C', 4:'D', 5:'E', 6:'F', 7:'G', 8:'H'}
        table = {}
        for row in self.board:
            for square in row:
                location = f'{row_letters[square.row]}{square.column}'
                table[location] = square
        return table

    def add_pieces(self):
        self.lookup_table['A8'].piece = Rook('b')
        self.lookup_table['B8'].piece = Knight('b')
        self.lookup_table['C8'].piece = Bishop('b')
        self.lookup_table['D8'].piece = Queen('b')
        self.lookup_table['E8'].piece = King('b')
        self.lookup_table['F8'].piece = Bishop('b')
        self.lookup_table['G8'].piece = Knight('b')
        self.lookup_table['H8'].piece = Rook('b')

        self.lookup_table['A7'].piece = Pawn('b')
        self.lookup_table['B7'].piece = Pawn('b')
        self.lookup_table['C7'].piece = Pawn('b')
        self.lookup_table['D7'].piece = Pawn('b')
        self.lookup_table['E7'].piece = Pawn('b')
        self.lookup_table['F7'].piece = Pawn('b')
        self.lookup_table['G7'].piece = Pawn('b')
        self.lookup_table['H7'].piece = Pawn('b')

        self.lookup_table['A1'].piece = Rook('w')
        self.lookup_table['B1'].piece = Knight('w')
        self.lookup_table['C1'].piece = Bishop('w')
        self.lookup_table['D1'].piece = Queen('w')
        self.lookup_table['E1'].piece = King('w')
        self.lookup_table['F1'].piece = Bishop('w')
        self.lookup_table['G1'].piece = Knight('w')
        self.lookup_table['H1'].piece = Rook('w')

        self.lookup_table['A2'].piece = Pawn('w')
        self.lookup_table['B2'].piece = Pawn('w')
        self.lookup_table['C2'].piece = Pawn('w')
        self.lookup_table['D2'].piece = Pawn('w')
        self.lookup_table['E2'].piece = Pawn('w')
        self.lookup_table['F2'].piece = Pawn('w')
        self.lookup_table['G2'].piece = Pawn('w')
        self.lookup_table['H2'].piece = Pawn('w')


    def __getitem__(self, location):
        return self.lookup_table[location]


    def __str__(self):
        printme = '    '
        for letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
            printme += f'{letter}      '
        printme += '\n'
        for index, row in enumerate(self.board):
            printme += f'{8-index} '
            for i in range(len(row)):
                printme+= '| ' + str(row[i]) + ' '
            printme += '|\n'
        return printme

class Player:
    def __init__(self, colour):
        self.colour = colour

if __name__ == "__main__":
    board = Board()
    print(board)
    board.add_pieces()
    print(board)
