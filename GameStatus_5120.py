"""
#Created on Tue Oct 14 10:45:10 2025

#@author: ELizabeth
#attempting to construct a local module called GameStatus_5120 to act 
#as custom class.  GameStatus actions acts as a blueprint to represent a 'tic-tac
#-toe game state
#citation: https://docs.python.org/3/tutorial/classes.html
"""

import numpy as np
import copy

class GameStatus:
    def __init__(self, board_state=None, turn_O=False):
        # Initialize board to 3x3 if not given
        if board_state is None:
            self.board_state = np.zeros((3, 3), dtype=int)
        else:
            self.board_state = np.array(board_state, dtype=int)

        self.turn_O = turn_O  # True = O’s turn (minimizer), False = X’s turn (maximizer)
        self.winner = None
        if self.board_state.shape != (3,3):
              raise ValueError("Board must be a 3X3 matrix.")

    # -------------------------------------------------------------------------
    def is_terminal(self):
        """
        Checks whether the game has reached a terminal state:
        - Win for X (1)
        - Win for O (-1)
        - Draw (no empty cells)
        Returns True if terminal, False otherwise.
        """
        # Check rows and columns
        for i in range(3):
            if abs(sum(self.board_state[i, :])) == 3:
                self.winner = 1 if sum(self.board_state[i, :]) == 3 else -1
                return True
            if abs(sum(self.board_state[:, i])) == 3:
                self.winner = 1 if sum(self.board_state[:, i]) == 3 else -1
                return True

        # Check diagonals
        diag1 = sum([self.board_state[i, i] for i in range(3)])
        diag2 = sum([self.board_state[i, 2 - i] for i in range(3)])
        if abs(diag1) == 3 or abs(diag2) == 3:
            self.winner = 1 if diag1 == 3 or diag2 == 3 else -1
            return True

        # Check for draw (no zeros)
        if not (0 in self.board_state):
            self.winner = 0
            return True

        return False

    # -------------------------------------------------------------------------
    def get_scores(self, _=None):
        """
        Returns a score based on the current game state:
        +1  if X (maximizer) wins
        -1  if O (minimizer) wins
         0  if draw or game not yet over
        """
        if self.winner == 1:
            return 1
        elif self.winner == -1:
            return -1
        else:
            return 0

    # -------------------------------------------------------------------------
    def get_negamax_scores(self, terminal):
        """
        Similar to get_scores(), but can assign larger magnitude values
        if desired for Negamax evaluation.
        """
        if self.winner == 1:
            return 100
        elif self.winner == -1:
            return -100
        else:
            return 0

    # -------------------------------------------------------------------------
    def get_moves(self):
        """
        Returns a list of all possible moves (empty cells) in (row, col) form.
        """
        moves = []
        for r in range(3):
            for c in range(3):
                if self.board_state[r, c] == 0:
                    moves.append((r, c))
        return moves

    # -------------------------------------------------------------------------
    def get_new_state(self, move):
        """
        Returns a new GameStatus object after applying the given move.
        X = +1, O = -1.
        """
        new_board = copy.deepcopy(self.board_state)
        x, y = move
        new_board[x, y] = -1 if self.turn_O else 1
        return GameStatus(new_board, not self.turn_O)

    # -------------------------------------------------------------------------
    def __repr__(self):
        return str(self.board_state)
