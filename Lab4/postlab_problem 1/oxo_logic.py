import os, random
import oxo_data

class Game:
    def __init__(self):
        """Initialize a new, empty game."""
        self.board = list(" " * 9)

    def save_game(self):
        """Save the current game state to disk."""
        oxo_data.saveGame(self.board)

    @classmethod
    def restore_game(cls):
        """Restore a previously saved game. If it fails, return a new game."""
        try:
            game = oxo_data.restoreGame()
            if len(game) == 9:
                new_game = cls()
                new_game.board = game
                return new_game
            else:
                return cls()
        except IOError:
            return cls()

    def _generate_move(self):
        """Generate a random cell from those available. 
        If all cells are used, return -1."""
        options = [i for i in range(len(self.board)) if self.board[i] == " "]
        if options:
            return random.choice(options)
        else:
            return -1

    def _is_winning_move(self):
        """Check for a winning move."""
        wins = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        )

        for a, b, c in wins:
            chars = self.board[a] + self.board[b] + self.board[c]
            if chars == 'XXX' or chars == 'OOO':
                return True
        return False

    def user_move(self, cell):
        """Process the user's move at the specified cell."""
        if self.board[cell] != ' ':
            raise ValueError('Invalid cell')
        else:
            self.board[cell] = 'X'
        if self._is_winning_move():
            return 'X'
        else:
            return ""

    def computer_move(self):
        """Generate and process the computer's move."""
        cell = self._generate_move()
        if cell == -1:
            return 'D'  # Draw
        self.board[cell] = 'O'
        if self._is_winning_move():
            return 'O'
        else:
            return ""

    def display(self):
        """Print the current board state."""
        print("Current board:")
        for i in range(0, 9, 3):
            print(" | ".join(self.board[i:i+3]))
            print("-" * 5)

def test():
    game = Game()
    result = ""
    while not result:
        game.display()
        try:
            cell = int(input("Enter your move (0-8): "))  # Assume user inputs a valid integer
            result = game.user_move(cell)
        except ValueError as e:
            print("Error:", e)
        if not result:
            result = game.computer_move()

        if not result:
            continue
        elif result == 'D':
            print("It's a draw!")
        else:
            print("Winner is:", result)
        game.display()

if __name__ == "__main__":
    test()