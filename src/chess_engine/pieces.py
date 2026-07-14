from .utils import is_square_under_attack

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

    def make_move(self, new_position, board):
        grid = board.board
        grid[self.position[0]][self.position[1]] = None
        grid[new_position[0]][new_position[1]] = self
        self.position = new_position
        self.has_moved = True
        board.side_to_move = "black" if self.color == "white" else "white"

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

    def make_move(self, new_position, board):
        grid = board.board
        grid[self.position[0]][self.position[1]] = None
        grid[new_position[0]][new_position[1]] = self
        self.position = new_position
        self.has_moved = True
        board.side_to_move = "black" if self.color == "white" else "white"
    
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

    def make_move(self, new_position, board):
        grid = board.board
        grid[self.position[0]][self.position[1]] = None
        grid[new_position[0]][new_position[1]] = self
        self.position = new_position
        self.has_moved = True
        board.side_to_move = "black" if self.color == "white" else "white"

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
    
    def make_move(self, new_position, board):
        if self.color == "white" and self.has_moved == False:
            if self.position == (0, 0):
                board.white_can_castle_queenside = False
            elif self.position == (0, 7):
                board.white_can_castle_kingside = False
        elif self.color == "black" and self.has_moved == False:
            if self.position == (7, 0):
                board.black_can_castle_queenside = False
            elif self.position == (7, 7):
                board.black_can_castle_kingside = False
        grid = board.board
        grid[self.position[0]][self.position[1]] = None
        grid[new_position[0]][new_position[1]] = self
        self.position = new_position
        self.has_moved = True
        board.side_to_move = "black" if self.color == "white" else "white"

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

    def make_move(self, new_position, board):
        grid = board.board
        grid[self.position[0]][self.position[1]] = None
        grid[new_position[0]][new_position[1]] = self
        self.position = new_position
        self.has_moved = True
        board.side_to_move = "black" if self.color == "white" else "white"

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
                if not is_square_under_attack(board, (new_row, new_col), "white" if self.color == "black" else "black"):
                    if target is None or target.color != self.color:
                        legal_moves.append((new_row, new_col))

        if not self.has_moved:
            if self.color == "white":
                if is_square_under_attack(board, (0, 3), "white"):
                    pass
                if board[0][7] is not None and isinstance(board[0][7], Rook) and not board[0][7].has_moved:
                    if board[0][5] is None and board[0][6] is None and not is_square_under_attack(board, (0, 5), "black") and not is_square_under_attack(board, (0, 6), "black"):
                        legal_moves.append((0, 6))
                if board[0][0] is not None and isinstance(board[0][0], Rook) and not board[0][0].has_moved:
                    if board[0][1] is None and board[0][2] is None and board[0][3] is None and not is_square_under_attack(board, (0, 2), "black") and not is_square_under_attack(board, (0, 3), "black"):
                        legal_moves.append((0, 2))
            else:
                if is_square_under_attack(board, (7, 3), "black"):
                    pass
                if board[7][7] is not None and isinstance(board[7][7], Rook) and not board[7][7].has_moved:
                    if board[7][5] is None and board[7][6] is None and not is_square_under_attack(board, (7, 5), "white") and not is_square_under_attack(board, (7, 6), "white"):
                        legal_moves.append((7, 6))
                if board[7][0] is not None and isinstance(board[7][0], Rook) and not board[7][0].has_moved:
                    if board[7][1] is None and board[7][2] is None and board[7][3] is None and not is_square_under_attack(board, (7, 2), "white") and not is_square_under_attack(board, (7, 3), "white"):
                        legal_moves.append((7, 2))

        return legal_moves

    def make_move(self, new_position, board):
        grid = board.board
        if new_position not in self.generate_legal_moves(grid):
            raise ValueError("Illegal move for the King.")

        old_row, old_col = self.position
        new_row, new_col = new_position
        y = 0 if self.color == "white" else 7

        # Move rook when castling
        if new_position == (y, 6) and not self.has_moved:
            rook = grid[y][7]
            if rook is None or not isinstance(rook, Rook) or rook.has_moved:
                raise ValueError("Cannot castle: Rook has moved or is not present.")
            else:
                rook.has_moved = True
                rook.position = (y, 5)
                grid[y][5] = rook
                grid[y][7] = None

        elif new_position == (y, 2) and not self.has_moved:
            rook = grid[y][0]
            if rook is None or not isinstance(rook, Rook) or rook.has_moved:
                raise ValueError("Cannot castle: Rook has moved or is not present.")
            else:
                rook.has_moved = True
                rook.position = (y, 3)
                grid[y][3] = rook
                grid[y][0] = None

        grid[old_row][old_col] = None
        grid[new_row][new_col] = self

        self.position = new_position
        self.has_moved = True

        if self.color == "white":
            board.white_can_castle_kingside = False
            board.white_can_castle_queenside = False
        elif self.color == "black":
            board.black_can_castle_kingside = False
            board.black_can_castle_queenside = False

        board.side_to_move = "black" if self.color == "white" else "white"



