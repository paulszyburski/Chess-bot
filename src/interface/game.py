import pygame

from chess_engine.board import Board

from .illustrate_board import BoardRenderer
from .settings import BOARD_SIZE


def main():
    pygame.init()

    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))

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


if __name__ == "__main__":
    main()
