
class Pawn:
    def __init__(self, color, position, board):
        self.color = color
        self.position = position
        self.board = board
        self.has_moved = False
    
    def generate_legal_moves(self):
        pass
        

class Bishop:
    def __init__(self, color, position, board):
        self.color = color
        self.position = position
        self.board = board

    def generate_legal_moves(self):
        pass

class Knight:
    def __init__(self, color, position, board):
        self.color = color
        self.position = position
        self.board = board

    def generate_legal_moves(self):
        pass

class Rook:
    def __init__(self, color, position, board):
        self.color = color
        self.position = position
        self.board = board
        self.has_moved = False

    def generate_legal_moves(self):
        pass

class Queen:
    def __init__(self, color, position, board):
        self.color = color
        self.position = position
        self.board = board

    def generate_legal_moves(self):
        pass

class King:
    def __init__(self, color, position, board):
        self.color = color
        self.position = position
        self.board = board
        self.has_moved = False

    def generate_legal_moves(self):
        pass
