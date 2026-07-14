
def translate_coordinates(coordinates):
    row = int(coordinates[1]) - 1
    col = ord(coordinates[0].lower()) - ord('a')
    return (row, col)

def is_square_under_attack(board, position, attacking_color):
    from .pieces import Pawn, Knight, Bishop, Rook, Queen, King

    target_row, target_col = position

    for row in range(8):
        for col in range(8):
            piece = board[row][col]

            if piece is None or piece.color != attacking_color:
                continue

            # Pawns attack diagonally, not forward
            if isinstance(piece, Pawn):
                direction = 1 if piece.color == "white" else -1

                if (
                    target_row == row + direction
                    and abs(target_col - col) == 1
                ):
                    return True

            elif isinstance(piece, Knight):
                row_distance = abs(target_row - row)
                col_distance = abs(target_col - col)

                if (row_distance, col_distance) in [(2, 1), (1, 2)]:
                    return True

            elif isinstance(piece, King):
                row_distance = abs(target_row - row)
                col_distance = abs(target_col - col)

                if max(row_distance, col_distance) == 1:
                    return True

            elif isinstance(piece, Bishop):
                directions = [
                    (1, 1), (1, -1),
                    (-1, 1), (-1, -1),
                ]

                if ray_attacks(
                    board,
                    (row, col),
                    position,
                    directions,
                ):
                    return True

            elif isinstance(piece, Rook):
                directions = [
                    (1, 0), (-1, 0),
                    (0, 1), (0, -1),
                ]

                if ray_attacks(
                    board,
                    (row, col),
                    position,
                    directions,
                ):
                    return True

            elif isinstance(piece, Queen):
                directions = [
                    (1, 0), (-1, 0),
                    (0, 1), (0, -1),
                    (1, 1), (1, -1),
                    (-1, 1), (-1, -1),
                ]

                if ray_attacks(
                    board,
                    (row, col),
                    position,
                    directions,
                ):
                    return True

    return False


def ray_attacks(board, start, target, directions):
    start_row, start_col = start

    for row_direction, col_direction in directions:
        row = start_row + row_direction
        col = start_col + col_direction

        while 0 <= row < 8 and 0 <= col < 8:
            if (row, col) == target:
                return True

            # Another piece blocks the attack
            if board[row][col] is not None:
                break

            row += row_direction
            col += col_direction

    return False



import numpy as np


def encode_board(board):
    piece_to_layer = {
        ("white", "P"): 0,
        ("white", "N"): 1,
        ("white", "B"): 2,
        ("white", "R"): 3,
        ("white", "Q"): 4,
        ("white", "K"): 5,

        ("black", "p"): 6,
        ("black", "n"): 7,
        ("black", "b"): 8,
        ("black", "r"): 9,
        ("black", "q"): 10,
        ("black", "k"): 11,
    }

    encoded = np.zeros((12, 8, 8), dtype=np.float32)

    for row in range(8):
        for col in range(8):
            piece = board[row][col]

            if piece is not None:
                layer = piece_to_layer[(piece.color, piece.symbol)]
                encoded[layer][row][col] = 1.0

    return encoded