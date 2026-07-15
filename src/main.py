import time

from bot.nn_bot import NNBot
from bot.nn import NN
from bot.search import search
import chess_engine.board as board
import chess_engine.utils as utils


def check_game_state(chess_board):
    color = chess_board.side_to_move

    if chess_board.is_checkmate(color):
        print(f"Checkmate! {color} loses.")
        return "checkmate"

    if chess_board.is_stalemate(color):
        print("Stalemate! It's a draw.")
        return "stalemate"

    if chess_board.is_in_check(color):
        print(f"{color} is in check!")
        return "check"

    return None


def game_is_over(chess_board):
    game_state = check_game_state(chess_board)

    return game_state in ("checkmate", "stalemate")


def get_bot_move(chess_bot, chess_board):
    """
    Runs search safely and returns:

        start, end, evaluation

    If no move is available, start and end will both be None.
    """
    result = search(chess_bot, chess_board)

    if result is None:
        return None, None, None

    move, evaluation = result

    if move is None:
        return None, None, evaluation

    start, end = move
    return start, end, evaluation


def nn_bot_vs_nn_bot():
    chess_board = board.Board()

    white_bot = NNBot(
        color="white",
        temperature=0.4,
    )

    black_bot = NNBot(
        color="black",
        temperature=0.4,
    )

    chess_board.display()

    while True:
        # Check whether the game already ended before White searches.
        if game_is_over(chess_board):
            break

        print("\nWhite Bot's turn:")

        start, end, evaluation = get_bot_move(
            white_bot,
            chess_board,
        )

        if start is None or end is None:
            print("No legal moves available for the white bot.")
            check_game_state(chess_board)
            break

        print(f"Bot's evaluation: {evaluation}")

        white_piece = chess_board.get_piece(start)

        if white_piece is None:
            print(f"Search returned an invalid starting square: {start}")
            break

        white_piece.make_move(end, chess_board)
        chess_board.display()

        # White may have checkmated or stalemated Black.
        if game_is_over(chess_board):
            break

        print("\nBlack Bot's turn:")

        start, end, evaluation = get_bot_move(
            black_bot,
            chess_board,
        )

        if start is None or end is None:
            print("No legal moves available for the black bot.")
            check_game_state(chess_board)
            break

        print(f"Bot's evaluation: {evaluation}")

        black_piece = chess_board.get_piece(start)

        if black_piece is None:
            print(f"Search returned an invalid starting square: {start}")
            break

        black_piece.make_move(end, chess_board)
        chess_board.display()

        # Black may have checkmated or stalemated White.
        if game_is_over(chess_board):
            break


def play_against_nn_bot():
    chess_board = board.Board()

    chess_bot = NNBot(
        color="black",
        temperature=0.0,
    )

    chess_board.display()

    while True:
        # Check whether the position is already over before player input.
        if game_is_over(chess_board):
            break

        move = input(
            "Pick your piece and move separated by space: "
        ).split()

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

        # The player's move may have ended the game.
        if game_is_over(chess_board):
            break

        print("\nBot's turn:")
        time.sleep(1)

        start, end, evaluation = get_bot_move(
            chess_bot,
            chess_board,
        )

        if start is None or end is None:
            print("No legal moves available for the bot.")
            check_game_state(chess_board)
            break

        print(f"Bot's evaluation: {evaluation}")

        bot_piece = chess_board.get_piece(start)

        if bot_piece is None:
            print(f"Search returned an invalid starting square: {start}")
            break

        bot_piece.make_move(end, chess_board)
        chess_board.display()

        # The bot's move may have ended the game.
        if game_is_over(chess_board):
            break


if __name__ == "__main__":
    ai = NN()

    # play_against_nn_bot()
    nn_bot_vs_nn_bot()