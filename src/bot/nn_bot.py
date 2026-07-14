import numpy as np

from .nn import NN


class NNBot:
    def __init__(self, color):
        self.color = color
        self.nn = NN()

    @staticmethod
    def encode_move(start, end):
        start_row, start_col = start
        end_row, end_col = end

        start_square = start_row * 8 + start_col
        end_square = end_row * 8 + end_col

        return start_square * 64 + end_square

    def choose_move(self, chess_board):
        legal_moves = []
        grid = chess_board.board

        for row in range(8):
            for col in range(8):
                piece = grid[row][col]

                if piece is not None and piece.color == self.color:
                    for end in piece.generate_legal_moves(grid):
                        legal_moves.append((piece.position, end))

        if not legal_moves:
            return None, None

        encoded_board = self.nn.encode_board(chess_board).reshape(1, -1)
        probabilities = self.nn.model.predict_proba(encoded_board)[0]

        probability_by_move = dict(
            zip(self.nn.model.classes_, probabilities)
        )

        return max(
            legal_moves,
            key=lambda move: probability_by_move.get(
                self.encode_move(move[0], move[1]),
                0.0,
            ),
        )