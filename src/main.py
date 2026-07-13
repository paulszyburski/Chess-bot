import chess_engine.board as board
import chess_engine.utils as utils
import bot.random_move as random_move

import time

def main():
    chess_board = board.Board()
    chess_bot = random_move.RandomBot(color="black")

    while True:
        move = input("Pick your piece and move seperated by space: ").split()
        if len(move) != 2:
            print("Invalid input. Please enter the piece and move separated by a space.")
            continue
        start, end = utils.translate_coordinates(move[0]), utils.translate_coordinates(move[1])
        print(start, end)

        piece = chess_board.get_piece(start)
        if piece is None or piece.color != "white":
            print("No piece at the starting position or not your piece.")
            continue
        legal_moves = piece.generate_legal_moves(chess_board.board)
        print(legal_moves)
        if end not in legal_moves:
            print("Illegal move for the selected piece.")
            continue

        piece.position = end
        chess_board.board[end[0]][end[1]] = piece
        chess_board.board[start[0]][start[1]] = None
        chess_board.display()
        print("\n\nBot's turn:")
        time.sleep(1)

        start, end = chess_bot.choose_move(chess_board.board)
        if start is None or end is None:
            print("No legal moves available for the bot.")
            break
        bot_piece = chess_board.get_piece(start)
        bot_piece.position = end
        chess_board.board[end[0]][end[1]] = bot_piece
        chess_board.board[start[0]][start[1]] = None
        chess_board.display()







if __name__ == "__main__":
    main()