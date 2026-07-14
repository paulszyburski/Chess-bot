import sys

import chess
import chess.pgn
import numpy as np


MAX_GAMES = 10_000
MAX_POSITIONS = 200_000
MIN_RATING = 1800


def encode_board(chess_board):
    """
    chess_board is your Board object, not chess_board.board.
    """

    encoded = np.zeros((17, 8, 8), dtype=np.int8)

    piece_to_layer = {
        "P": 0,
        "N": 1,
        "B": 2,
        "R": 3,
        "Q": 4,
        "K": 5,
    }

    for row in range(8):
        for col in range(8):
            piece = chess_board.board[row][col]

            if piece is None:
                continue

            layer = piece_to_layer[piece.symbol.upper()]

            if piece.color == "black":
                layer += 6

            encoded[layer][row][col] = 1

    if chess_board.side_to_move == "white":
        encoded[12].fill(1)

    if chess_board.white_can_castle_kingside:
        encoded[13].fill(1)

    if chess_board.white_can_castle_queenside:
        encoded[14].fill(1)

    if chess_board.black_can_castle_kingside:
        encoded[15].fill(1)

    if chess_board.black_can_castle_queenside:
        encoded[16].fill(1)

    return encoded.flatten()

def encode_move(move):
    """
    Move numbers range from 0 to 4095.

    Example:
    e2e4 = starting square * 64 + destination square
    """
    return move.from_square * 64 + move.to_square


def rating_is_high_enough(game):
    try:
        white_rating = int(game.headers.get("WhiteElo", 0))
        black_rating = int(game.headers.get("BlackElo", 0))
    except ValueError:
        return False

    return white_rating >= MIN_RATING and black_rating >= MIN_RATING


def create_dataset():
    positions = []
    moves = []

    games_processed = 0

    while (
        games_processed < MAX_GAMES
        and len(positions) < MAX_POSITIONS
    ):
        game = chess.pgn.read_game(sys.stdin)

        if game is None:
            break

        games_processed += 1

        if not rating_is_high_enough(game):
            continue

        board = game.board()

        for move in game.mainline_moves():
            # Include promotion moves. The promotion piece is intentionally
            # ignored by encode_move(), so every promotion is learned as the
            # same start-square -> end-square move. The engine automatically
            # promotes to a queen when that move is played.
            positions.append(encode_board(board))
            moves.append(encode_move(move))

            board.push(move)

            if len(positions) >= MAX_POSITIONS:
                break

        if games_processed % 1000 == 0:
            print(
                f"Games: {games_processed}, "
                f"positions: {len(positions)}",
                file=sys.stderr,
            )

    if not positions:
        raise RuntimeError("No training positions were created.")

    X = np.asarray(positions, dtype=np.int8)
    y = np.asarray(moves, dtype=np.uint16)

    np.savez_compressed(
        "lichess_training_data.npz",
        X=X,
        y=y,
    )

    print(
        f"Saved {len(X)} positions.\n"
        f"X shape: {X.shape}\n"
        f"y shape: {y.shape}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    create_dataset()