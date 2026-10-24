import io
import unittest
from unittest.mock import patch

import chess
import numpy as np

from bot.create_dataset import create_dataset
from bot.nn import NN
from bot.nn_bot import NNBot
from bot.search import search
from chess_engine.board import Board
from chess_engine.utils import translate_coordinates


class ChessTests(unittest.TestCase):
    def test_initial_position(self):
        board = Board()
        self.assertEqual(len(board.get_all_legal_moves("white")), 20)
        np.testing.assert_array_equal(
            NN.encode_board(board), NN.encode_training_board(chess.Board())
        )

    def test_illegal_move_leaves_board_unchanged(self):
        board = Board()
        before = NN.encode_board(board)
        with self.assertRaises(ValueError):
            board.make_move((1, 4), (4, 4))
        np.testing.assert_array_equal(before, NN.encode_board(board))

    def test_coordinates(self):
        self.assertEqual(translate_coordinates("E4"), (3, 4))
        for square in ("", "a0", "i4", "a10", "aa"):
            with self.subTest(square=square), self.assertRaises(ValueError):
                translate_coordinates(square)

    def test_checkmate_has_no_bot_moves(self):
        board = Board()
        for start, end in (("f2", "f3"), ("e7", "e5"), ("g2", "g4"), ("d8", "h4")):
            board.make_move(translate_coordinates(start), translate_coordinates(end))
        self.assertEqual(board.get_game_state(), "checkmate")
        bot = object.__new__(NNBot)
        bot.color = "white"
        self.assertEqual(search(bot, board), (None, None))

    def test_dataset_from_pgn(self):
        pgn = '[WhiteElo "2000"]\n[BlackElo "2000"]\n\n1. e4 e5 *\n'
        with (
            patch("sys.stdin", io.StringIO(pgn)),
            patch("numpy.savez_compressed") as save,
        ):
            create_dataset()
        data = save.call_args.kwargs
        self.assertEqual(data["X"].shape, (2, 1088))
        self.assertEqual(data["y"].tolist(), [796, 3364])

    def test_search_returns_legal_move(self):
        board = Board()
        before = NN.encode_board(board)
        bot = NNBot("white", temperature=0)
        move, score = search(bot, board, top_n=2, search_depth=1)
        self.assertIn(move, board.get_all_legal_moves("white"))
        self.assertTrue(np.isfinite(score))
        self.assertEqual(bot.color, "white")
        np.testing.assert_array_equal(before, NN.encode_board(board))


if __name__ == "__main__":
    unittest.main()
