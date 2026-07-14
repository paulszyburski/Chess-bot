import io
from contextlib import contextmanager
from pathlib import Path

import chess
import chess.pgn
import joblib
import numpy as np
import zstandard as zstd
from sklearn.neural_network import MLPClassifier


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
MODEL_PATH = DATA_DIR / "chess_model.joblib"

MAX_GAMES = 100_000
MAX_POSITIONS = 10_000_000
MIN_RATING = 1200
BATCH_SIZE = 2048


class NN:
    def __init__(self):
        self.model = None
        DATA_DIR.mkdir(exist_ok=True)

        if MODEL_PATH.exists():
            self.load_model(MODEL_PATH)
        elif self.data_files():
            self.train()

    def data_files(self):
        return sorted(DATA_DIR.glob("*.pgn")) + sorted(DATA_DIR.glob("*.pgn.zst"))

    @contextmanager
    def open_pgn(self, path):
        if path.suffix == ".zst":
            with path.open("rb") as compressed:
                with zstd.ZstdDecompressor().stream_reader(
                    compressed,
                    read_across_frames=True,
                ) as reader:
                    with io.TextIOWrapper(
                        reader,
                        encoding="utf-8",
                        errors="replace",
                    ) as text:
                        yield text
        else:
            with path.open("r", encoding="utf-8", errors="replace") as text:
                yield text

    @staticmethod
    def encode_training_board(board):
        encoded = np.zeros((17, 8, 8), dtype=np.float32)

        for square, piece in board.piece_map().items():
            row = chess.square_rank(square)
            col = chess.square_file(square)
            layer = piece.piece_type - 1

            if piece.color == chess.BLACK:
                layer += 6

            encoded[layer][row][col] = 1

        if board.turn == chess.WHITE:
            encoded[12].fill(1)
        if board.has_kingside_castling_rights(chess.WHITE):
            encoded[13].fill(1)
        if board.has_queenside_castling_rights(chess.WHITE):
            encoded[14].fill(1)
        if board.has_kingside_castling_rights(chess.BLACK):
            encoded[15].fill(1)
        if board.has_queenside_castling_rights(chess.BLACK):
            encoded[16].fill(1)

        return encoded.flatten()

    @staticmethod
    def encode_board(board):
        """Encode your own chess_engine.board.Board object."""
        encoded = np.zeros((17, 8, 8), dtype=np.float32)
        piece_layers = {"P": 0, "N": 1, "B": 2, "R": 3, "Q": 4, "K": 5}

        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]

                if piece is not None:
                    layer = piece_layers[piece.symbol.upper()]
                    if piece.color == "black":
                        layer += 6
                    encoded[layer][row][col] = 1

        if board.side_to_move == "white":
            encoded[12].fill(1)
        if board.white_can_castle_kingside:
            encoded[13].fill(1)
        if board.white_can_castle_queenside:
            encoded[14].fill(1)
        if board.black_can_castle_kingside:
            encoded[15].fill(1)
        if board.black_can_castle_queenside:
            encoded[16].fill(1)

        return encoded.flatten()

    @staticmethod
    def encode_move(move):
        return move.from_square * 64 + move.to_square

    @staticmethod
    def rating_is_high_enough(game):
        try:
            return (
                int(game.headers.get("WhiteElo", 0)) >= MIN_RATING
                and int(game.headers.get("BlackElo", 0)) >= MIN_RATING
            )
        except ValueError:
            return False

    def train_batch(self, positions, moves, first_batch):
        X = np.asarray(positions, dtype=np.float32)
        y = np.asarray(moves, dtype=np.int32)

        if first_batch:
            self.model.partial_fit(X, y, classes=np.arange(4096))
        else:
            self.model.partial_fit(X, y)

    def train(self):
        files = self.data_files()

        if not files:
            print(f"No .pgn or .pgn.zst files found in {DATA_DIR}")
            return

        self.model = MLPClassifier(
            hidden_layer_sizes=(128,),
            batch_size=256,
            random_state=42,
        )

        positions = []
        moves = []
        games_processed = 0
        positions_processed = 0
        first_batch = True

        for path in files:
            print(f"Reading {path.name}")

            with self.open_pgn(path) as pgn:
                while (
                    games_processed < MAX_GAMES
                    and positions_processed < MAX_POSITIONS
                ):
                    game = chess.pgn.read_game(pgn)

                    if game is None:
                        break

                    games_processed += 1

                    if not self.rating_is_high_enough(game):
                        continue

                    board = game.board()

                    for move in game.mainline_moves():
                        # Ignore positions involving en passant and promotion.
                        if board.ep_square is None and move.promotion is None:
                            positions.append(self.encode_training_board(board))
                            moves.append(self.encode_move(move))
                            positions_processed += 1

                        board.push(move)

                        if len(positions) >= BATCH_SIZE:
                            self.train_batch(positions, moves, first_batch)
                            first_batch = False
                            positions.clear()
                            moves.clear()
                            print(
                                f"Games: {games_processed} | "
                                f"positions: {positions_processed}"
                            )

                        if positions_processed >= MAX_POSITIONS:
                            break

            if (
                games_processed >= MAX_GAMES
                or positions_processed >= MAX_POSITIONS
            ):
                break

        if positions:
            self.train_batch(positions, moves, first_batch)
            first_batch = False

        if first_batch:
            raise RuntimeError("No usable training positions were found.")

        self.save_model(MODEL_PATH)
        print(f"Saved model to {MODEL_PATH}")

    def load_model(self, model_path=MODEL_PATH):
        self.model = joblib.load(model_path)

    def save_model(self, model_path=MODEL_PATH):
        joblib.dump(self.model, model_path)

    def predict(self, board):
        if self.model is None:
            raise RuntimeError("The model has not been trained.")

        encoded = self.encode_board(board).reshape(1, -1)
        return int(self.model.predict(encoded)[0])


if __name__ == "__main__":
    NN()