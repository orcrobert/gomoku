import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.game import Game
import numpy as np
from domain.board import Board
from services.ai import AI

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_init(self):
        self.assertEqual(self.game.board_height, 15)
        self.assertEqual(self.game.board_width, 15)
        self.assertEqual(self.game.player, 0)
        self.assertEqual(self.game.game_over, False)

    def test_change_player(self):
        self.game.change_player()
        self.assertEqual(self.game.player, 1)

    def test_is_valid_move(self):
        self.assertTrue(self.game.is_valid_move(0, 0))
        self.assertFalse(self.game.is_valid_move(15, 15))

    def test_add_remove_move(self):
        self.game.add_move(0, 0)
        self.assertEqual(self.game.board[0][0], 0)
        self.game.remove_move(0, 0)
        self.assertEqual(self.game.board[0][0], -1)

    def test_has_nearby_moves(self):
        self.game.add_specific_move(0, 0, 1)
        self.assertTrue(self.game.has_nearby_moves(0, 1))
        self.assertFalse(self.game.has_nearby_moves(3, 3))

    def test_search_winning_move(self):
        self.game.player = 1
        for _ in range(4):
            self.game.add_specific_move(0, _, 1)
        self.assertTrue(self.game.search_winning_move())

    def test_search_blocking_move(self):
        for _ in range(4):
            self.game.add_specific_move(0, _, 0)
        self.assertTrue(self.game.search_blocking_move())

    def test_search_nearby_move(self):
        self.game.add_specific_move(0, 0, 1)
        self.assertTrue(self.game.search_nearby_move())

    def test_make_random_move(self):
        self.game.make_random_move()
        self.assertTrue(any(self.game.board[r][c] == 0 for r in range(self.game.board_height) for c in range(self.game.board_width)))

    def test_make_computer_move(self):
        self.game.make_computer_move()
        self.assertTrue(any(self.game.board[r][c] == 0 for r in range(self.game.board_height) for c in range(self.game.board_width)))

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_init(self):
        self.assertEqual(self.board.height, 15)
        self.assertEqual(self.board.width, 15)
        self.assertIsNone(self.board.last_move)
        np.testing.assert_array_equal(self.board.board, np.full((15, 15), -1, dtype=int))

    def test_element(self):
        self.assertEqual(self.board.element(0, 0), -1)

    def test_add_move(self):
        self.board.add_move(0, 0, 1)
        self.assertEqual(self.board.element(0, 0), 1)
        self.assertEqual(self.board.last_move, (0, 0))

    def test_remove_move(self):
        self.board.add_move(0, 0, 1)
        self.board.remove_move(0, 0)
        self.assertEqual(self.board.element(0, 0), -1)
        
class TestAI(unittest.TestCase):
    def setUp(self):
        self.ai = AI()

    def test_init(self):
        self.assertEqual(self.ai.board_height, 15)
        self.assertEqual(self.ai.board_width, 15)
        self.assertEqual(self.ai.player, 0)
        self.assertEqual(self.ai.game_over, False)

    def test_change_player(self):
        self.ai.change_player()
        self.assertEqual(self.ai.player, 1)

    def test_is_valid_move(self):
        self.assertTrue(self.ai.is_valid_move(0, 0))
        self.assertFalse(self.ai.is_valid_move(15, 15))

    def test_is_board_full(self):
        self.assertFalse(self.ai.is_board_full())

    def test_generate_moves(self):
        self.ai.add_move(0, 0)
        self.ai.add_move(0, 1)
        self.assertIn((0, 2), self.ai.generate_moves())

    def test_get_neighbors(self):
        self.assertIn((0, 1), self.ai.get_neighbors(0, 0))

    def test_is_winner(self):
        self.assertFalse(self.ai.is_winner(self.ai.PLAYER))
        self.assertFalse(self.ai.is_winner(self.ai.COMPUTER))

    def test_add_remove_move(self):
        self.ai.add_move(0, 0)
        self.assertEqual(self.ai.board[0][0], 0)
        self.ai.remove_move(0, 0)
        self.assertEqual(self.ai.board[0][0], -1)
        
if __name__ == '__main__':
    unittest.main()