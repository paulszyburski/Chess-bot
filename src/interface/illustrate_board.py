import pygame

from .settings import (
    BOARD_SIZE,
    SQUARE_SIZE,
    LIGHT_SQUARE_COLOR,
    DARK_SQUARE_COLOR,
)


class BoardRenderer:
    def __init__(self, screen, board):
        self.screen = screen
        self.board_surface = self.create_board_surface()
        self.board = board

    def create_board_surface(self):
        surface = pygame.Surface((BOARD_SIZE, BOARD_SIZE))

        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    color = LIGHT_SQUARE_COLOR
                else:
                    color = DARK_SQUARE_COLOR

                square = pygame.Rect(
                    col * SQUARE_SIZE,
                    row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE,
                )

                pygame.draw.rect(surface, color, square)

        return surface
    
    def draw_pieces(self, board):
        for row in range(8):
            for col in range(8):
                piece = board[row][col]

                if piece is None:
                    continue

                piece_name = piece.color.upper()[0] + piece.symbol.lower()

                piece_image = pygame.image.load(f'assets/{piece_name}.png')
                piece_image = pygame.transform.scale(piece_image,
                                                     (SQUARE_SIZE, SQUARE_SIZE))

                displayed_row = 7 - row

                x = col * SQUARE_SIZE
                y = displayed_row * SQUARE_SIZE

                self.screen.blit(piece_image, (x, y))



    def draw(self):
        self.screen.blit(self.board_surface, (0, 0))
        self.draw_pieces(self.board)

