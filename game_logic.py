# This file will contain the game logic
# such as the board and game state
# as well as functions to update the board, check for a win, and check for a draw.

class NewGame:
    def __init__(self):
        # initialize empty 3x3 board
        self.board = [
            [0,0,0],
            [0,0,0],
            [0,0,0]
            ]           # 0 is empty space. 1 is 'O', 2 is 'X'
        self.moves = 0  # number of moves made
        self.player = 1 # player 1's turn initially

    # winning lines
    WINS = (
        [(0,0), (0,1), (0,2)],     # row 1
        [(1,0), (1,1), (1,2)],     # row 2
        [(2,0), (2,1), (2,2)],     # row 3
        [(0,0), (1,0), (2,0)],     # col 1
        [(0,1), (1,1), (2,1)],     # col 2
        [(0,2), (1,2), (2,2)],     # col 3
        [(0,0), (1,1), (2,2)],     # diag1
        [(0,2), (1,1), (2,0)]      # diag2
        )

    def check_win(self) -> tuple[int]:
        """Checks the current board state and number of moves to see if any player has won.
        
        Returns -1 if game is a draw, 0 if it is incomplete, 1 if player 1 ('O') wins, and 2 if player 2 ('X') wins."""
        winner = 0            # intial winner is 0, meaning game is incomplete
        win_type = -1         # type of win: -1 if draw, else refer to which line of WINS it applies to

        for line_no, line in enumerate(self.WINS):           # iterate thru every victory line (rows, cols, and diags)
            prod = 1                # product, if a line is completed, product must be 1*1*1 = 1 or 2*2*2 = 8
            for row, col in line:
                prod *= self.board[row][col]     # check board and update product
            # check wins
            if prod == 1:
                winner = 1
                win_type = line_no
                break
                # player 1 wins
            elif prod == 8:                # 2*2*2
                winner = 2
                win_type = line_no
                break
                # player 2 wins
        
        # check for draw
        if winner == 0 and self.moves == 9:     # max moves but still no winner
            winner = -1
            win_type = -1

        return winner, win_type

    def check_available(self, square) -> bool:
        """Given board state and target square (0-8), return True if the square is available (unoccupied)"""
        selected_row = square//3        # row
        selected_col = square%3         # col
        # unoccupied
        if self.board[selected_row][selected_col] == 0:
            return True
        return False

    def make_move(self, square) -> None:
        """Given target square (0-8), update board to include new move and also update whose turn it is"""
        selected_row = square//3        # row
        selected_col = square%3         # col

        self.board[selected_row][selected_col] = self.player
        self.player = (0, 2, 1)[self.player]                # switch player each time a move is made
        self.moves += 1             # increment moves made
