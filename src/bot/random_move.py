
class RandomBot:
    def __init__(self, color):
        self.color = color

    def choose_move(self, board):
        import random
        legal_moves = []

        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.color == self.color:
                    moves = piece.generate_legal_moves(board)
                    for move in moves:
                        legal_moves.append((piece.position, move))

        if legal_moves:
            return random.choice(legal_moves)
        else:
            return None, None