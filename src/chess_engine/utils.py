
def translate_coordinates(coordinates):
    row = int(coordinates[1]) - 1
    col = ord(coordinates[0].lower()) - ord('a')
    return (row, col)

def is_square_under_attack(board, position, attacking_color):
    from pieces import King
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