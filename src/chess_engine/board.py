
from pieces import Pawn, Rook, Knight, Bishop, Queen, King

class Board:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        # Initialize an 8x8 chess board with pieces in starting positions
        board = [[{} for _ in range(8)] for _ in range(8)]
        
        for column in range(8):
            board[1][column]["P"] = Pawn("white", (1, column), board=board)
        
        board[0][0]["R"] = Rook("white", (0, 0), board=board)
        board[0][1]["N"] = Knight("white", (0, 1), board=board)
        board[0][2]["B"] = Bishop("white", (0, 2), board=board)
        board[0][3]["Q"] = Queen("white", (0, 3), board=board)
        board[0][4]["K"] = King("white", (0, 4), board=board)
        board[0][5]["B"] = Bishop("white", (0, 5), board=board)
        board[0][6]["N"] = Knight("white", (0, 6), board=board)
        board[0][7]["R"] = Rook("white", (0, 7), board=board)

        for column in range(8):
            board[6][column]["p"] = Pawn("black", (6, column), board=board)

        board[7][0]["r"] = Rook("black", (7, 0), board=board)
        board[7][1]["n"] = Knight("black", (7, 1), board=board)
        board[7][2]["b"] = Bishop("black", (7, 2), board=board)
        board[7][3]["q"] = Queen("black", (7, 3), board=board)
        board[7][4]["k"] = King("black", (7, 4), board=board)
        board[7][5]["b"] = Bishop("black", (7, 5), board=board)
        board[7][6]["n"] = Knight("black", (7, 6), board=board)
        board[7][7]["r"] = Rook("black", (7, 7), board=board)

        return board

    def display(self):
        for row in reversed(self.board):
            print(" ".join(next(iter(square), ".") for square in row))
        
    def get_piece(self, position):
        col, row = position
        return list(self.board[row][col].values())[0] if self.board[row][col] else None
    

if __name__ == "__main__":
    chess_board = Board()
    chess_board.display()
    print(chess_board.get_piece((2, 0)))
