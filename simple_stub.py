# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 15:41:25 2025

@author: warre
"""

"""
Author: Elizabeth Warren
Course: CSE 4050 – Web Application Development / AI Project
Description: Minimal working stub that connects GameStatus, Minimax, and GUI logic.
"""

import pygame
from GameStatus_5120 import GameStatus
from multiAgent import minimax


class SimpleTicTacToe:
    """Minimal working version of Tic Tac Toe with Minimax AI."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("Tic Tac Toe (Stub)")
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_turn = 'X'
        self.game_state = GameStatus(self.board)
        self.running = True

    def draw_board(self):
        self.screen.fill((0, 0, 0))
        color = (255, 255, 255)
        for i in range(1, 3):
            pygame.draw.line(self.screen, color, (0, i * 133), (400, i * 133), 3)
            pygame.draw.line(self.screen, color, (i * 133, 0), (i * 133, 400), 3)
        pygame.display.update()

    def is_game_over(self):
        terminal = self.game_state.is_terminal()
        if terminal:
            final_scores = self.game_state.get_scores(terminal)
            print(f"🏁 Game Over! Final Scores: {final_scores}")
            return True
        return False

    def move(self, move):
        """Sync logical GameStatus with board after each move."""
        self.game_state = self.game_state.get_new_state(move)

    def play_ai(self):
        """Very simple AI using Minimax for demonstration."""
        score, move = minimax(self.game_state, depth=2, maximizingPlayer=False)
        if move:
            r, c = move
            self.board[r][c] = 'O'
            self.move(move)
            print(f"🤖 AI chose {move} (score={score})")

    def play_game(self):
        """Simple playable loop."""
        self.draw_board()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONUP and self.current_turn == 'X':
                    x, y = pygame.mouse.get_pos()
                    row, col = y // 133, x // 133
                    if self.board[row][col] == '':
                        self.board[row][col] = 'X'
                        self.move((row, col))
                        if self.is_game_over():
                            pygame.time.wait(1000)
                            self.running = False
                            break

                        self.current_turn = 'O'
                        self.play_ai()

                        if self.is_game_over():
                            pygame.time.wait(1000)
                            self.running = False
                            break

            pygame.display.update()

        print("👋 Exiting game.")
        pygame.quit()


# --- Quick test harness ---
if __name__ == "__main__":
    game = SimpleTicTacToe()
    game.play_game()
