import sys

import chess
import chess.pgn
import numpy as np

from bot.nn import NN

encode_board = NN.encode_training_board
encode_move = NN.encode_move


MAX_GAMES = 10_000
MAX_POSITIONS = 200_000
MIN_RATING = 1800


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

    while games_processed < MAX_GAMES and len(positions) < MAX_POSITIONS:
        game = chess.pgn.read_game(sys.stdin)

        if game is None:
            break

        games_processed += 1

        if not rating_is_high_enough(game):
            continue

        board = game.board()

        for move in game.mainline_moves():
            positions.append(encode_board(board))
            moves.append(encode_move(move))

            board.push(move)

            if len(positions) >= MAX_POSITIONS:
                break

        if games_processed % 1000 == 0:
            print(
                f"Games: {games_processed}, positions: {len(positions)}",
                file=sys.stderr,
            )

    if not positions:
        raise RuntimeError("No training positions were created.")

    X = np.asarray(positions, dtype=np.int8)
    y = np.asarray(moves, dtype=np.uint16)

    np.savez_compressed("lichess_training_data.npz", X=X, y=y)

    print(
        f"Saved {len(X)} positions.\nX shape: {X.shape}\ny shape: {y.shape}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    create_dataset()
