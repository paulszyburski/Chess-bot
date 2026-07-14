
from .pieces import Pawn, Rook, Knight, Bishop, Queen, King
from .utils import is_square_under_attack


class Board:
    def __init__(self):
        self.board = self.create_board()
        self.side_to_move = "white"

        self.white_can_castle_kingside = True
        self.white_can_castle_queenside = True
        self.black_can_castle_kingside = True
        self.black_can_castle_queenside = True

    def create_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]

        for column in range(8):
            board[1][column] = Pawn(
                color="white",
                position=(1, column),
            )

        board[0][0] = Rook("white", (0, 0))
        board[0][1] = Knight("white", (0, 1))
        board[0][2] = Bishop("white", (0, 2))
        board[0][3] = Queen("white", (0, 3))
        board[0][4] = King("white", (0, 4))
        board[0][5] = Bishop("white", (0, 5))
        board[0][6] = Knight("white", (0, 6))
        board[0][7] = Rook("white", (0, 7))

        for column in range(8):
            board[6][column] = Pawn(
                color="black",
                position=(6, column),
            )

        board[7][0] = Rook("black", (7, 0))
        board[7][1] = Knight("black", (7, 1))
        board[7][2] = Bishop("black", (7, 2))
        board[7][3] = Queen("black", (7, 3))
        board[7][4] = King("black", (7, 4))
        board[7][5] = Bishop("black", (7, 5))
        board[7][6] = Knight("black", (7, 6))
        board[7][7] = Rook("black", (7, 7))

        return board

    def display(self):
        for row in reversed(self.board):
            for piece in row:
                if piece is None:
                    print(".", end=" ")
                else:
                    print(piece.symbol, end=" ")

            print()

    def get_piece(self, position):
        row, col = position

        if not (0 <= row < 8 and 0 <= col < 8):
            return None

        return self.board[row][col]

    @staticmethod
    def opposite_color(color):
        if color == "white":
            return "black"

        return "white"

    def find_king(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]

                if isinstance(piece, King) and piece.color == color:
                    return piece

        return None

    def is_in_check(self, color):
        king = self.find_king(color)

        if king is None:
            raise ValueError(f"Could not find the {color} king.")

        enemy_color = self.opposite_color(color)

        return is_square_under_attack(
            self.board,
            king.position,
            enemy_color,
        )

    def move_causes_check(self, piece, new_position):

        old_position = piece.position

        old_row, old_col = old_position
        new_row, new_col = new_position

        captured_piece = self.board[new_row][new_col]

        self.board[old_row][old_col] = None
        self.board[new_row][new_col] = piece
        piece.position = new_position

        king_is_in_check = self.is_in_check(piece.color)

        self.board[old_row][old_col] = piece
        self.board[new_row][new_col] = captured_piece
        piece.position = old_position

        return king_is_in_check

    def get_legal_moves(self, piece):

        if piece is None:
            return []

        legal_moves = []

        possible_moves = piece.generate_legal_moves(self.board)

        for new_position in possible_moves:
            target_piece = self.get_piece(new_position)

            if isinstance(target_piece, King):
                continue

            if not self.move_causes_check(piece, new_position):
                legal_moves.append(new_position)

        return legal_moves

    def get_all_legal_moves(self, color):
        legal_moves = []

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]

                if piece is None or piece.color != color:
                    continue

                moves = self.get_legal_moves(piece)

                for new_position in moves:
                    legal_moves.append(
                        (piece.position, new_position)
                    )

        return legal_moves

    def has_legal_moves(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]

                if piece is None or piece.color != color:
                    continue

                if self.get_legal_moves(piece):
                    return True

        return False

    def is_checkmate(self, color):
        return (
            self.is_in_check(color)
            and not self.has_legal_moves(color)
        )

    def is_stalemate(self, color):
        return (
            not self.is_in_check(color)
            and not self.has_legal_moves(color)
        )

    def get_game_state(self):

        color = self.side_to_move

        if self.is_checkmate(color):
            return "checkmate"

        if self.is_stalemate(color):
            return "stalemate"

        if self.is_in_check(color):
            return "check"

        return "playing"

    def disable_castling_for_captured_rook(
        self,
        captured_piece,
        captured_position,
    ):
        if not isinstance(captured_piece, Rook):
            return

        if captured_piece.color == "white":
            if captured_position == (0, 0):
                self.white_can_castle_queenside = False

            elif captured_position == (0, 7):
                self.white_can_castle_kingside = False

        elif captured_piece.color == "black":
            if captured_position == (7, 0):
                self.black_can_castle_queenside = False

            elif captured_position == (7, 7):
                self.black_can_castle_kingside = False

    def make_move(self, start_position, new_position):
        piece = self.get_piece(start_position)

        if piece is None:
            raise ValueError(
                f"There is no piece at {start_position}."
            )

        if piece.color != self.side_to_move:
            raise ValueError(
                f"It is {self.side_to_move}'s turn."
            )

        legal_moves = self.get_legal_moves(piece)

        if new_position not in legal_moves:
            raise ValueError(
                f"{start_position} to {new_position} is illegal."
            )

        captured_piece = self.get_piece(new_position)

        piece.make_move(new_position, self)

        self.disable_castling_for_captured_rook(
            captured_piece,
            new_position,
        )

    def quick_test(self):
        piece = self.board[0][2]
        return self.get_legal_moves(piece)

    

if __name__ == "__main__":
    chess_board = Board()
    chess_board.display()
    print(chess_board.get_piece((4,1)))
    print(chess_board.quick_test())
