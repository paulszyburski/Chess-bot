import numpy as np

from .nn import NN


class NNBot:
    def __init__(self, color, temperature=1.0):
        self.color = color
        self.temperature = temperature
        self.nn = NN()

    def encode_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end

        start_square = start_row * 8 + start_col
        end_square = end_row * 8 + end_col

        return start_square * 64 + end_square
    
    def list_top_n_moves(self, chess_board, n=5):
        legal_moves = chess_board.get_all_legal_moves(self.color)

        if not legal_moves:
            return None, None

        encoded_board = self.nn.encode_board(
            chess_board
        ).reshape(1, -1)

        probabilities = self.nn.model.predict_proba(encoded_board)[0]

        probability_by_move = dict(
            zip(self.nn.model.classes_, probabilities)
        )

        legal_move_probabilities = np.array(
            [
                probability_by_move.get(
                    self.encode_move(start, end),
                    0.0
                )
                for start, end in legal_moves
            ],
            dtype=np.float64
        )

        n = max(0, min(n, len(legal_moves)))

        if n == 0:
            return []

        top_indexes = np.argsort(legal_move_probabilities)[::-1][:n]

        top_moves = [
            legal_moves[index]
            for index in top_indexes
        ]

        return top_moves


    def choose_move(self, chess_board):
        legal_moves = chess_board.get_all_legal_moves(self.color)

        if not legal_moves:
            return None, None

        encoded_board = self.nn.encode_board(
            chess_board
        ).reshape(1, -1)

        probabilities = self.nn.model.predict_proba(encoded_board)[0]

        probability_by_move = dict(
            zip(self.nn.model.classes_, probabilities)
        )

        legal_move_probabilities = np.array(
            [
                probability_by_move.get(
                    self.encode_move(start, end),
                    0.0
                )
                for start, end in legal_moves
            ],
            dtype=np.float64
        )

        # Temperature 0 means always choose the best move.
        if self.temperature <= 0:
            best_index = np.argmax(legal_move_probabilities)
            return legal_moves[best_index]

        # Prevent log(0).
        legal_move_probabilities = np.clip(
            legal_move_probabilities,
            1e-12,
            None
        )

        # Apply temperature.
        log_probabilities = np.log(legal_move_probabilities)
        log_probabilities /= self.temperature

        # Prevent overflow in exp().
        log_probabilities -= np.max(log_probabilities)

        adjusted_probabilities = np.exp(log_probabilities)
        adjusted_probabilities /= adjusted_probabilities.sum()

        chosen_index = np.random.choice(
            len(legal_moves),
            p=adjusted_probabilities
        )

        return legal_moves[chosen_index]