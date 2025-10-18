# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 16:50:51 2025

@author: warre
full game
"""
"""
Author: Elizabeth Warren
Simple Tic Tac Toe Stub (Full Game Version)
Plays alternating turns between Player (X=1) and AI (O=-1)
"""

import pygame
import numpy as np
from GameStatus_5120 import GameStatus
from multiAgent import minimax


class SimpleTicTacToe:
    """Minimal working version of Tic Tac Toe with Minimax AI."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("Tic Tac Toe (Stub)")
        self.board = np.zeros((3, 3), dtype=int)   # 0 = empty
        self.current_turn = 1                      # 1 = Player (X), -1 = AI (O)
        self.game_state = GameStatus(self.board)
        self.running = True

    def draw_board(self):
        self.screen.fill((0, 0, 0))
        color = (255, 255, 255)
        for i in range(1, 3):
            pygame.draw.line(self.screen, color, (0, i * 133), (400, i * 133), 3)
            pygame.draw.line(self.screen, color, (i * 133, 0), (i * 133, 400), 3)
        pygame.display.update()

    def draw_symbol(self, row, col, value):
        cx, cy = col * 133 + 66, row * 133 + 66
        if value == 1:  # X
            pygame.draw.line(self.screen, (255, 0, 0), (cx - 40, cy - 40), (cx + 40, cy + 40), 4)
            pygame.draw.line(self.screen, (255, 0, 0), (cx + 40, cy - 40), (cx - 40, cy + 40), 4)
        elif value == -1:  # O
            pygame.draw.circle(self.screen, (0, 255, 0), (cx, cy), 45, 4)
        pygame.display.update()

    def is_game_over(self):
        terminal = self.game_state.is_terminal()
        if terminal:
            final_scores = self.game_state.get_scores(terminal)
            print(f"🏁 Game Over! Final Scores: {final_scores}")
            return True
        return False

    def move(self, move, value):
        """Apply move and sync logical GameStatus."""
        row, col = move
        self.board[row][col] = value
        self.game_state = self.game_state.get_new_state(move)

    def play_ai(self):
        """AI uses Minimax algorithm to choose next move."""
        score, move = minimax(self.game_state, depth=2, maximizingPlayer=False)
        if move:
            r, c = move
            self.move(move, -1)
            self.draw_symbol(r, c, -1)
            print(f"🤖 AI chose {move} (score={score})")

    def play_game(self):
        """Playable loop — alternates between player and AI until terminal."""
        self.draw_board()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONUP and self.current_turn == 1:
                    x, y = pygame.mouse.get_pos()
                    row, col = y // 133, x // 133

                    # Skip invalid clicks
                    if row > 2 or col > 2 or self.board[row][col] != 0:
                        continue

                    # Player move (1)
                    self.move((row, col), 1)
                    self.draw_symbol(row, col, 1)

                    if self.is_game_over():
                        pygame.time.wait(1500)
                        self.running = False
                        break

                    # Switch to AI
                    self.current_turn = -1
                    pygame.display.update()

                    # AI move
                    self.play_ai()

                    if self.is_game_over():
                        pygame.time.wait(1500)
                        self.running = False
                        break

                    # 🔁 Switch back to player
                    self.current_turn = 1

            pygame.display.update()

        print("👋 Exiting game.")
        pygame.quit()


# --- Quick test harness ---
if __name__ == "__main__":
    game = SimpleTicTacToe()
    game.play_game()
