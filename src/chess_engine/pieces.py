from narwhals import col

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
        if new_position not in self.generate_legal_moves(board.board):
            raise ValueError("Illegal move for the Pawn.")

        grid = board.board
        grid[self.position[0]][self.position[1]] = None
        if (self.color == "white" and new_position[0] == 7) or (self.color == "black" and new_position[0] == 0):
            self.symbol = "Q" if self.color == "white" else "q"
            grid[new_position[0]][new_position[1]] = Queen(self.color, new_position)
        else:
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
        if new_position not in self.generate_legal_moves(board.board):
            raise ValueError("Illegal move for the Bishop.")
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
        if new_position not in self.generate_legal_moves(board.board):
            raise ValueError("Illegal move for the Knight.")
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
        if new_position not in self.generate_legal_moves(board.board):
            raise ValueError("Illegal move for the Rook.")
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
        if new_position not in self.generate_legal_moves(board.board):
            raise ValueError("Illegal move for the Queen.")
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
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]

        for row_change, col_change in directions:
            new_row = row + row_change
            new_col = col + col_change

            if not (
                0 <= new_row < 8
                and 0 <= new_col < 8
            ):
                continue

            target_piece = board[new_row][new_col]

            if (
                target_piece is None
                or target_piece.color != self.color
            ):
                legal_moves.append((new_row, new_col))

        enemy_color = (
            "black"
            if self.color == "white"
            else "white"
        )

        home_row = 0 if self.color == "white" else 7
        starting_position = (home_row, 4)

        king_is_on_starting_square = (
            self.position == starting_position
        )

        king_is_currently_checked = is_square_under_attack(
            board,
            self.position,
            enemy_color,
        )

        if (
            not self.has_moved
            and king_is_on_starting_square
            and not king_is_currently_checked
        ):
            self.add_kingside_castling_move(
                board,
                legal_moves,
                home_row,
                enemy_color,
            )

            self.add_queenside_castling_move(
                board,
                legal_moves,
                home_row,
                enemy_color,
            )

        return legal_moves

    def add_kingside_castling_move(
        self,
        board,
        legal_moves,
        home_row,
        enemy_color,
    ):
        rook = board[home_row][7]

        valid_rook = (
            isinstance(rook, Rook)
            and rook.color == self.color
            and not rook.has_moved
        )

        squares_are_empty = (
            board[home_row][5] is None
            and board[home_row][6] is None
        )

        king_passes_through_check = (
            is_square_under_attack(
                board,
                (home_row, 5),
                enemy_color,
            )
            or is_square_under_attack(
                board,
                (home_row, 6),
                enemy_color,
            )
        )

        if (
            valid_rook
            and squares_are_empty
            and not king_passes_through_check
        ):
            legal_moves.append((home_row, 6))

    def add_queenside_castling_move(
        self,
        board,
        legal_moves,
        home_row,
        enemy_color,
    ):
        rook = board[home_row][0]

        valid_rook = (
            isinstance(rook, Rook)
            and rook.color == self.color
            and not rook.has_moved
        )

        squares_are_empty = (
            board[home_row][1] is None
            and board[home_row][2] is None
            and board[home_row][3] is None
        )

        king_passes_through_check = (
            is_square_under_attack(
                board,
                (home_row, 3),
                enemy_color,
            )
            or is_square_under_attack(
                board,
                (home_row, 2),
                enemy_color,
            )
        )

        if (
            valid_rook
            and squares_are_empty
            and not king_passes_through_check
        ):
            legal_moves.append((home_row, 2))

    def make_move(self, new_position, board):

        if new_position not in board.get_legal_moves(self):
            raise ValueError("Illegal move for the king.")

        grid = board.board

        old_row, old_col = self.position
        new_row, new_col = new_position

        home_row = 0 if self.color == "white" else 7

        is_kingside_castling = (
            not self.has_moved
            and self.position == (home_row, 4)
            and new_position == (home_row, 6)
        )

        is_queenside_castling = (
            not self.has_moved
            and self.position == (home_row, 4)
            and new_position == (home_row, 2)
        )

        if is_kingside_castling:
            rook = grid[home_row][7]

            if (
                not isinstance(rook, Rook)
                or rook.color != self.color
                or rook.has_moved
            ):
                raise ValueError(
                    "Cannot castle: invalid kingside rook."
                )

            grid[home_row][7] = None
            grid[home_row][5] = rook

            rook.position = (home_row, 5)
            rook.has_moved = True

        elif is_queenside_castling:
            rook = grid[home_row][0]

            if (
                not isinstance(rook, Rook)
                or rook.color != self.color
                or rook.has_moved
            ):
                raise ValueError(
                    "Cannot castle: invalid queenside rook."
                )

            grid[home_row][0] = None
            grid[home_row][3] = rook

            rook.position = (home_row, 3)
            rook.has_moved = True

        grid[old_row][old_col] = None
        grid[new_row][new_col] = self

        self.position = new_position
        self.has_moved = True

        if self.color == "white":
            board.white_can_castle_kingside = False
            board.white_can_castle_queenside = False
            board.side_to_move = "black"

        else:
            board.black_can_castle_kingside = False
            board.black_can_castle_queenside = False
            board.side_to_move = "white"

