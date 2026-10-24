def translate_coordinates(coordinates):
    coordinates = coordinates.lower()
    if (
        len(coordinates) != 2
        or coordinates[0] not in "abcdefgh"
        or coordinates[1] not in "12345678"
    ):
        raise ValueError("Use squares from a1 to h8.")
    row = int(coordinates[1]) - 1
    col = ord(coordinates[0].lower()) - ord("a")
    return (row, col)


def is_square_under_attack(board, position, attacking_color):
    from .pieces import Bishop, King, Knight, Pawn, Queen, Rook

    target_row, target_col = position

    for row in range(8):
        for col in range(8):
            piece = board[row][col]

            if piece is None or piece.color != attacking_color:
                continue

            if isinstance(piece, Pawn):
                direction = 1 if piece.color == "white" else -1

                if target_row == row + direction and abs(target_col - col) == 1:
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
                directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

                if ray_attacks(board, (row, col), position, directions):
                    return True

            elif isinstance(piece, Rook):
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

                if ray_attacks(board, (row, col), position, directions):
                    return True

            elif isinstance(piece, Queen):
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

                if ray_attacks(board, (row, col), position, directions):
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

            if board[row][col] is not None:
                break

            row += row_direction
            col += col_direction

    return False
