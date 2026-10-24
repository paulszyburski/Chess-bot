import copy

from bot.evaluation import evaluate


def search(bot, chess_board, top_n=5, search_depth=3):
    original_bot_color = bot.color

    top_moves = bot.list_top_n_moves(chess_board, n=top_n)

    if not top_moves:
        return None, None

    best_move = None
    best_evaluation = float("-inf")

    for move in top_moves:
        simulated_board = copy.deepcopy(chess_board)

        start, end = move
        simulated_board.make_move(start, end)

        for _ in range(search_depth):
            game_state = simulated_board.get_game_state()

            if game_state in ("checkmate", "stalemate"):
                break

            bot.color = simulated_board.side_to_move

            predicted_move = bot.choose_move(simulated_board)

            if predicted_move == (None, None):
                break

            predicted_start, predicted_end = predicted_move

            simulated_board.make_move(predicted_start, predicted_end)

        game_state = simulated_board.get_game_state()

        position_evaluation = evaluate(
            simulated_board.board,
            checkmate=game_state == "checkmate",
            stalemate=game_state == "stalemate",
            side_to_move=simulated_board.side_to_move,
        )

        if original_bot_color == "white":
            bot_evaluation = position_evaluation
        else:
            bot_evaluation = -position_evaluation

        if bot_evaluation > best_evaluation:
            best_evaluation = bot_evaluation
            best_move = move

    bot.color = original_bot_color

    return best_move, best_evaluation
