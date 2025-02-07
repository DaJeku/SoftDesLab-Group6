import unittest
from oxo_logic import Game

class TestTicTacToeGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_new_game(self):
        self.assertEqual(self.game.board, [" "] * 9, "New game should have an empty board")

    def test_user_move_valid(self):
        result = self.game.user_move(0)
        self.assertEqual(self.game.board[0], "X", "User move should place 'X' on the board")
        self.assertEqual(result, "", "Valid move should not end the game")

    def test_user_move_invalid(self):
        self.game.user_move(0)
        with self.assertRaises(ValueError):
            self.game.user_move(0)

    def test_computer_move(self):
        result = self.game.computer_move()
        self.assertIn("O", self.game.board, "Computer move should place 'O' on the board")
        self.assertIn(result, ["", "O", "D"], "Computer move should return valid result")

    def test_winning_move_horizontal(self):
        self.game.board = ["X", "X", " ", "O", "O", " ", " ", " ", " "]
        result = self.game.user_move(2)
        self.assertEqual(result, "X", "Horizontal win should be detected")

    def test_winning_move_vertical(self):
        self.game.board = ["O", "X", " ", "O", "X", " ", " ", " ", " "]
        result = self.game.user_move(6)
        self.assertEqual(result, "X", "Vertical win should be detected")

    def test_winning_move_diagonal(self):
        self.game.board = ["X", "O", " ", " ", "X", "O", " ", " ", " "]
        result = self.game.user_move(8)
        self.assertEqual(result, "X", "Diagonal win should be detected")

    def test_draw_game(self):
        self.game.board = ["X", "O", "X", "X", "O", "O", "O", "X", " "]
        result = self.game.computer_move()
        self.assertEqual(result, "D", "Draw game should be detected")

    def test_save_and_restore_game(self):
        self.game.board = ["X", "O", " ", " ", "X", " ", " ", " ", "O"]
        self.game.save_game()
        
        new_game = Game()
        new_game.restore_game()
        
        self.assertEqual(new_game.board, self.game.board, "Game state should be correctly saved and restored")

    def test_generate_move(self):
        self.game.board = ["X", "O", "X", "O", "X", "O", " ", " ", " "]
        move = self.game._generate_move()
        self.assertIn(move, [6, 7, 8], "Generated move should be one of the available spaces")

    def test_is_winning_move(self):
        self.game.board = ["X", "X", "X", "O", "O", " ", " ", " ", " "]
        self.assertTrue(self.game._is_winning_move(), "Winning move should be detected")

        self.game.board = ["X", "O", "X", "O", "O", "X", " ", " ", " "]
        self.assertFalse(self.game._is_winning_move(), "Non-winning board should not be detected as a win")

if __name__ == '__main__':
    unittest.main()