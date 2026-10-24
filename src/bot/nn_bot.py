import numpy as np

from .nn import NN


class NNBot:
    def __init__(self, color, temperature=1.0, nn=None):
        self.color = color
        self.temperature = temperature
        self.nn = nn if nn is not None else NN()
        if self.nn.model is None:
            raise RuntimeError("Missing model: place chess_model.joblib in src/data.")

    def encode_move(self, start, end):
        start_square = start[0] * 8 + start[1]
        end_square = end[0] * 8 + end[1]
        return start_square * 64 + end_square

    def move_probabilities(self, board):
        moves = board.get_all_legal_moves(self.color)
        if not moves:
            return [], np.array([])
        encoded = self.nn.encode_board(board).reshape(1, -1)
        probabilities = self.nn.model.predict_proba(encoded)[0]
        by_move = dict(zip(self.nn.model.classes_, probabilities))
        weights = np.array(
            [by_move.get(self.encode_move(*move), 0.0) for move in moves]
        )
        return moves, weights

    def list_top_n_moves(self, board, n=5):
        moves, weights = self.move_probabilities(board)
        indexes = np.argsort(weights)[::-1][: max(0, n)]
        return [moves[index] for index in indexes]

    def choose_move(self, board):
        moves, weights = self.move_probabilities(board)
        if not moves:
            return None, None
        if self.temperature <= 0:
            return moves[np.argmax(weights)]

        logits = np.log(np.clip(weights, 1e-12, None)) / self.temperature
        weights = np.exp(logits - logits.max())
        weights /= weights.sum()
        return moves[np.random.choice(len(moves), p=weights)]
