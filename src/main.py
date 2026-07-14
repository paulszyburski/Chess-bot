import time

from bot.nn_bot import NNBot
from bot.nn import NN
import chess_engine.board as board
import chess_engine.utils as utils


def check_game_state(chess_board):
    color = chess_board.side_to_move

    if chess_board.is_checkmate(color):
        print(f"Checkmate! {color} loses.")
        return True

    if chess_board.is_stalemate(color):
        print("Stalemate! It's a draw.")
        return True

    if chess_board.is_in_check(color):
        print(f"{color} is in check!")

    return False

def nn_bot_vs_nn_bot():
    chess_board = board.Board()
    white_bot = NNBot(color="white", temperature=0.0)
    black_bot = NNBot(color="black", temperature=0.0)

    chess_board.display()

    while True:
        print("\nWhite Bot's turn:")
        time.sleep(1)

        start, end = white_bot.choose_move(chess_board)

        if start is None or end is None:
            print("No legal moves available for the white bot.")
            break

        white_piece = chess_board.get_piece(start)
        white_piece.make_move(end, chess_board)
        chess_board.display()

        if check_game_state(chess_board):
            break

        print("\nBlack Bot's turn:")
        time.sleep(1)

        start, end = black_bot.choose_move(chess_board)

        if start is None or end is None:
            print("No legal moves available for the black bot.")
            break

        black_piece = chess_board.get_piece(start)
        black_piece.make_move(end, chess_board)
        chess_board.display()

        if check_game_state(chess_board):
            break


def play_against_nn_bot():
    chess_board = board.Board()
    chess_bot = NNBot(color="black")

    chess_board.display()

    while True:
        move = input("Pick your piece and move separated by space: ").split()

        if len(move) != 2:
            print("Invalid input. Enter something like: e2 e4")
            continue

        start = utils.translate_coordinates(move[0])
        end = utils.translate_coordinates(move[1])

        piece = chess_board.get_piece(start)

        if piece is None or piece.color != "white":
            print("No white piece at the starting position.")
            continue

        piece.make_move(end, chess_board)
        chess_board.display()

        if check_game_state(chess_board):
            break

        print("\nBot's turn:")
        time.sleep(1)

        start, end = chess_bot.choose_move(chess_board)

        if start is None or end is None:
            print("No legal moves available for the bot.")
            break

        bot_piece = chess_board.get_piece(start)
        bot_piece.make_move(end, chess_board)
        chess_board.display()

        if check_game_state(chess_board):
            break


if __name__ == "__main__":
    ai = NN()
    #play_against_nn_bot()
    nn_bot_vs_nn_bot()