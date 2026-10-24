import sys

from bot.nn_bot import NNBot
from bot.search import search
from chess_engine.board import Board
from chess_engine.utils import translate_coordinates


def check_game_state(board):
    state = board.get_game_state()
    if state == "checkmate":
        print(f"Checkmate! {board.side_to_move} loses.")
    elif state == "stalemate":
        print("Stalemate! It's a draw.")
    elif state == "check":
        print(f"{board.side_to_move} is in check.")
    return state


def play_bot_turn(bot, board):
    move, evaluation = search(bot, board)
    if move is None:
        return False
    print(f"{bot.color.capitalize()} bot: {move}, evaluation: {evaluation}")
    board.make_move(*move)
    return True


def play(watch=False):
    board = Board()
    bots = {"black": NNBot("black", temperature=0.4 if watch else 0.0)}
    if watch:
        bots["white"] = NNBot("white", temperature=0.4, nn=bots["black"].nn)
    board.display()

    while check_game_state(board) not in ("checkmate", "stalemate"):
        if board.side_to_move in bots:
            if not play_bot_turn(bots[board.side_to_move], board):
                break
        else:
            move = input("Your move (e2 e4), or q to quit: ").strip()
            if move.lower() == "q":
                break
            if len(move.split()) != 2:
                print("Enter two squares, like e2 e4.")
                continue
            try:
                start, end = move.split()
                board.make_move(
                    translate_coordinates(start), translate_coordinates(end)
                )
            except ValueError as error:
                print(f"Invalid move: {error}")
                continue
        board.display()


if __name__ == "__main__":
    mode = sys.argv[1:]
    if mode not in ([], ["watch"], ["board"]):
        sys.exit("Usage: python src/main.py [watch|board]")
    try:
        if mode == ["board"]:
            from interface.game import main

            main()
        else:
            play(watch=mode == ["watch"])
    except (KeyboardInterrupt, EOFError):
        print("\nGame closed.")
