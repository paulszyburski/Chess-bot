import pygame

from .settings import (
    BOARD_SIZE,
    SQUARE_SIZE,
    LIGHT_SQUARE_COLOR,
    DARK_SQUARE_COLOR,
)

from .illustrate_board import BoardRenderer
from chess_engine.board import Board

def main():
    pygame.init()

    screen = pygame.display.set_mode(
        (BOARD_SIZE, BOARD_SIZE)
    )

    pygame.display.set_caption("Chess Board")


    board = Board()
    board_renderer = BoardRenderer(screen, board.board)
    

    clock = pygame.time.Clock()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        board_renderer.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()