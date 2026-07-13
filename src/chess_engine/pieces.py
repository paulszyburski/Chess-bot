
class Pawn:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.has_moved = False
        self.symbol = "P" if color == "white" else "p"
    
    def generate_legal_moves(self, board):
        legal_moves = []

        row, col = self.position

        direction = 1 if self.color == "white" else -1

        if board[row + direction][col] is None:
            legal_moves.append((row + direction, col))

            if not self.has_moved and board[row + 2 * direction][col] is None:
                legal_moves.append((row + 2 * direction, col))

        for offset in [-1, 1]:
            new_col = col + offset
            new_row = row + direction

            if 0 <= new_col < 8:
                target = board[new_row][new_col]

                if target is not None and target.color != self.color:
                    legal_moves.append((new_row, new_col))

        return legal_moves

class Bishop:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.symbol = "B" if color == "white" else "b"

    def generate_legal_moves(self, board):
        legal_moves = []

        row, col = self.position

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for d_row, d_col in directions:
            new_row, new_col = row + d_row, col + d_col

            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]

                if target is None:
                    legal_moves.append((new_row, new_col))
                elif target.color != self.color:
                    legal_moves.append((new_row, new_col))
                    break
                else:
                    break

                new_row += d_row
                new_col += d_col
        return legal_moves
    
class Knight:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.symbol = "N" if color == "white" else "n"

    def generate_legal_moves(self, board):
        legal_moves = []
        row, col = self.position

        directions = [
            (row + 2, col + 1), (row + 2, col - 1),
            (row - 2, col + 1), (row - 2, col - 1),
            (row + 1, col + 2), (row + 1, col - 2),
            (row - 1, col + 2), (row - 1, col - 2)
        ]

        for new_row, new_col in directions:
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target is None or target.color != self.color:
                    legal_moves.append((new_row, new_col))

        return legal_moves

class Rook:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.has_moved = False
        self.symbol = "R" if color == "white" else "r"

    def generate_legal_moves(self, board):
        legal_moves = []

        row, col = self.position

        directions = [(1,0), (-1,0), (0,1), (0,-1)]

        for new_row, new_col in directions:
            new_row, new_col = row + new_row, col + new_col

            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]

                if target is None:
                    legal_moves.append((new_row, new_col))
                elif target.color != self.color:
                    legal_moves.append((new_row, new_col))
                    break
                else:
                    break

                new_row += new_row
                new_col += new_col
        return legal_moves

class Queen:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.symbol = "Q" if color == "white" else "q"

    def generate_legal_moves(self, board):
        legal_moves = []

        row, col = self.position
        
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        for d_row, d_col in directions:
            new_row, new_col = row + d_row, col + d_col

            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]

                if target is None:
                    legal_moves.append((new_row, new_col))
                elif target.color != self.color:
                    legal_moves.append((new_row, new_col))
                    break
                else:
                    break

                new_row += d_row
                new_col += d_col
        return legal_moves

class King:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.has_moved = False
        self.symbol = "K" if color == "white" else "k"

    def generate_legal_moves(self, board):
        legal_moves = []
        row, col = self.position

        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        for d_row, d_col in directions:
            new_row, new_col = row + d_row, col + d_col

            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target is None or target.color != self.color:
                    legal_moves.append((new_row, new_col))

        return legal_moves
