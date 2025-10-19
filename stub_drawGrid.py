# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 11:38:17 2025
@author: warre
Tiny stub just calls draw_game(self)
->just want to see the grid render without starting the whole game loop.
"""

# stub_runner.py
import pygame
from large_board_tic_tac_toe import RandomBoardTicTacToe  # your file

if __name__ == "__main__":
    app = RandomBoardTicTacToe(size=(600, 600))
    app.draw_game()          # 🔹 just draw the grid once
    running = True

    # Minimal event pump so the window stays responsive
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()