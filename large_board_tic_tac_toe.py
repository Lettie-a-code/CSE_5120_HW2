"""


Created on Fri Oct 17 13:45:11 2025
@author: warre
Both player and AI uses is_game_over() instead of seperate is_terminal() cals
real world moves:
player moves->check moves->AI moves->check game
self.move keeps GameStatus updated after both player and AI actions
No longer handle final_scores or terminal logic twice
"""

import numpy as np
import sys, random
import pygame
from multiAgent import minimax, negamax
from GameStatus_5120 import GameStatus

import numpy as np
import sys, random
import pygame
from multiAgent import minimax, negamax
from GameStatus_5120 import GameStatus

class RandomBoardTicTacToe:
    """Tic Tac Toe game with Minimax and Negamax AI modes."""

    def __init__(self, size=(600, 600)):
        pygame.init()
        self.size = size
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Tic Tac Toe – Player vs AI")

        # Grid settings
        self.GRID_SIZE = 3
        self.WIDTH = 150
        self.HEIGHT = 150
        self.MARGIN = 10

        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)

        # Game state variables
        self.board = [['' for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        self.current_turn = 'X'
        self.algorithm_choice = "Minimax"  # Can switch to "Negamax"
        self.game_state = GameStatus(self.board)

        self.draw_game()

    def draw_game(self):
        """Draw the game grid."""
        self.screen.fill(self.BLACK)
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                rect = pygame.Rect(
                    col * (self.WIDTH + self.MARGIN) + self.MARGIN,
                    row * (self.HEIGHT + self.MARGIN) + self.MARGIN,
                    self.WIDTH,
                    self.HEIGHT
                )
                pygame.draw.rect(self.screen, self.WHITE, rect, 2)
        pygame.display.update()

    def change_turn(self):
        """Toggle between X (player) and O (AI)."""
        self.current_turn = 'O' if self.current_turn == 'X' else 'X'
        pygame.display.set_caption(f"Tic Tac Toe – Turn: {self.current_turn}")

    def draw_X(self, row, col):
        """Draw an X (player move)."""
        x_start = col * (self.WIDTH + self.MARGIN) + self.MARGIN
        y_start = row * (self.HEIGHT + self.MARGIN) + self.MARGIN

        pygame.draw.line(
            self.screen, self.RED,
            (x_start + 10, y_start + 10),
            (x_start + self.WIDTH - 10, y_start + self.HEIGHT - 10), 5)
        pygame.draw.line(
            self.screen, self.RED,
            (x_start + self.WIDTH - 10, y_start + 10),
            (x_start + 10, y_start + self.HEIGHT - 10), 5)
        pygame.display.update()

    def draw_O(self, row, col):
        """Draw an O (AI move)."""
        cell_x = col * (self.WIDTH + self.MARGIN) + self.MARGIN + self.WIDTH // 2
        cell_y = row * (self.HEIGHT + self.MARGIN) + self.MARGIN + self.HEIGHT // 2
        pygame.draw.circle(self.screen, self.GREEN, (int(cell_x), int(cell_y)), int(self.WIDTH // 2.5), 5)
        pygame.display.update()

    def game_reset(self):
        """Clear board and reset state."""
        self.board = [['' for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        self.current_turn = 'X'
        self.game_state = GameStatus(self.board)
        self.draw_game()
        
    def move(self, move):
        """Update the internal GameStatus after applying a move."""
        self.game_state = self.game_state.get_new_state(move)

    def is_game_over(self):
        """
        Check whether the game has ended using GameStatus logic.
        Returns True if terminal, otherwise False.
        """
        terminal = self.game_state.is_terminal()
        if terminal:
            final_scores = self.game_state.get_scores(terminal)
            print(f"🏁 Game Over detected! Final Scores: {final_scores}")
            return True
        return False

    def play_game(self, mode="player_vs_ai"):
        """Main event loop that manages gameplay."""
        clock = pygame.time.Clock()
        running = True
        self.game_reset()
        print(f"🎮 Game started in mode: {mode}")
        print(f"🧮 Using {self.algorithm_choice} algorithm.")
        
        while running:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return

                elif event.type == pygame.MOUSEBUTTONUP and self.current_turn == "X":
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // (self.WIDTH + self.MARGIN)
                    row = pos[1] // (self.HEIGHT + self.MARGIN)

                    # 🧱 Guard: ignore clicks outside the grid
                    if row >= self.GRID_SIZE or col >= self.GRID_SIZE:
                        continue

                    # 🚫 Guard: prevent overwriting existing move
                    if self.board[row][col] != '':
                        print("⚠️ Cell already filled. Choose another.")
                        continue

                    # 🎯 Player (X) move
                    self.board[row][col] = 'X'
                    self.draw_X(row, col)
                    self.move((row, col))  # update logical GameStatus state

                    # 🏁 Check if game over (wrapper call)
                    if self.is_game_over():
                        pygame.time.wait(1500)
                        self.game_reset()
                        continue

                    # 🔄 Switch turn
                    self.change_turn()

                    # 🤖 AI Turn
                    if mode == "player_vs_ai" and self.current_turn == "O":
                        score, move = self.play_ai()

                        # 🧩 Ensure GameStatus is synchronized after AI move
                        if move:
                            self.move(move)

                        # 🏁 Check again after AI move
                        if self.is_game_over():
                            pygame.time.wait(1500)
                            self.game_reset()
                            continue

            pygame.display.update()

        print("👋 Exiting game loop.")
        pygame.quit()

    def play_ai(self):
        """AI move using Minimax or Negamax (based on self.algorithm_choice)."""
        score, move = None, None

        if self.algorithm_choice == "Minimax":
            score, move = minimax(
                self.game_state,
                depth=4,
                maximizingPlayer=False,
                alpha=float('-inf'),
                beta=float('inf'),
                indent=""
            )
            print(f"🧠 Minimax chose move {move} (score={score})")

        elif self.algorithm_choice == "Negamax":
            score, move = negamax(
                self.game_state,
                depth=4,
                alpha=float('-inf'),
                beta=float('inf'),
                color=-1,
                indent=""
            )
            print(f"🧠 Negamax chose move {move} (score={score})")

        else:
            print("⚠️ Unknown algorithm choice; defaulting to Minimax.")
            score, move = minimax(
                self.game_state,
                depth=4,
                maximizingPlayer=False,
                alpha=float('-inf'),
                beta=float('inf'),
                indent=""
            )

        # Apply move if valid
        if move:
            row, col = move
            if self.board[row][col] == '':
                self.board[row][col] = 'O'
                self.draw_O(row, col)
                self.move((row, col))  #<-Sync GameStatus
                
        terminal = self.game_state.is_terminal()
        if terminal:
            final_scores = self.game_state.get_scores(terminal)
            print(f"🏁 Final Scores: {final_scores}")
        else:
            self.change_turn()

        pygame.display.update()
        return score, move
       
    def wait_for_exit(self):
        """Keep window open until closed."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()
# 🧪 Test harness: runs automatically if launched directly
if __name__ == "__main__":
    tictactoe = RandomBoardTicTacToe()
    tictactoe.play_game(mode="player_vs_ai")

