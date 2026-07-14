
def translate_coordinates(coordinates):
    row = int(coordinates[1]) - 1
    col = ord(coordinates[0].lower()) - ord('a')
    return (row, col)

def is_square_under_attack(board, position, attacking_color):
    from .pieces import King
    target_row, target_col = position

    for row in range(8):
        for col in range(8):
            piece = board[row][col]

            if piece is None or piece.color != attacking_color:
                continue

            if isinstance(piece, King):
                row_distance = abs(target_row - row)
                col_distance = abs(target_col - col)

                if row_distance <= 1 and col_distance <= 1:
                    return True

            elif position in piece.generate_legal_moves(board):
                return True

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