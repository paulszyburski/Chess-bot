def evaluate(board, checkmate, stalemate, side_to_move):
    piece_to_points = {
        "p": 1,
        "b": 3,
        "n": 3,
        "r": 5,
        "q": 9,
    }

    if stalemate:
        return 0

    if checkmate:
        if side_to_move == "black":
            # Black has been checkmated, so White won.
            return 10000

        if side_to_move == "white":
            # White has been checkmated, so Black won.
            return -10000

    white_sum = 0
    black_sum = 0

    for row in range(8):
        for col in range(8):
            square = board[row][col]

            if square is None:
                continue

            piece = square.symbol.lower()
            color = square.color

            if piece == "k":
                continue

            if color == "white":
                white_sum += piece_to_points[piece]
            else:
                black_sum += piece_to_points[piece]

    return white_sum - black_sum