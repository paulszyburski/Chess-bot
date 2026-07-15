import pygame

from .settings import BOARD_SIZE, SQUARE_SIZE


class InputHandler:
    def __init__(self):
        self.selected_position = None
        self.legal_moves = []

    def mouse_to_board_position(self, mouse_position):
        mouse_x, mouse_y = mouse_position

        col = mouse_x // SQUARE_SIZE
        displayed_row = mouse_y // SQUARE_SIZE

        row = 7 - displayed_row

        return row, col

    def handle_event(self, event, chess_board):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        if event.button != 1:
            return

        position = self.mouse_to_board_position(event.pos)

        if self.selected_position is None:
            self.select_piece(chess_board, position)
        else:
            self.try_move(chess_board, position)

