
from .pieces import Pawn, Rook, Knight, Bishop, Queen, King

class Board:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        # Initialize an 8x8 chess board with pieces in starting positions
        board = [[None for _ in range(8)] for _ in range(8)]
        
        for column in range(8):
            board[1][column] = Pawn("white", (1, column))
        
        board[0][0] = Rook(color="white", position=(0, 0))
        board[0][1] = Knight(color="white", position=(0, 1))
        board[0][2] = Bishop(color="white", position=(0, 2))
        board[0][3] = Queen(color="white", position=(0, 3))
        board[0][4] = King(color="white", position=(0, 4))
        board[0][5] = Bishop(color="white", position=(0, 5))
        board[0][6] = Knight(color="white", position=(0, 6))
        board[0][7] = Rook(color="white", position=(0, 7))

        for column in range(8):
            board[6][column] = Pawn(color="black", position=(6, column))

        board[7][0] = Rook(color="black", position=(7, 0))
        board[7][1] = Knight(color="black", position=(7, 1))
        board[7][2] = Bishop(color="black", position=(7, 2))
        board[7][3] = Queen(color="black", position=(7, 3))
        board[7][4] = King(color="black", position=(7, 4))
        board[7][5] = Bishop(color="black", position=(7, 5))
        board[7][6] = Knight(color="black", position=(7, 6))
        board[7][7] = Rook(color="black", position=(7, 7))

        return board

    def display(self):
        for row in reversed(self.board):
            for piece in row:
                if piece is None:
                    print(".", end=" ")
                else:
                    print(piece.symbol, end=" ")
            print()
        
    def get_piece(self, position):
        row, col = position
        return self.board[row][col] if self.board[row][col] else None
    
    def quick_test(self):
        return self.board[0][2].generate_legal_moves(self.board)

if __name__ == "__main__":
    chess_board = Board()
    chess_board.display()
    print(chess_board.get_piece((4,1)))
    print(chess_board.quick_test())
