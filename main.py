import pygame
import os

from game_logic import *
from user_interface import *

def run_game():
    clock = pygame.time.Clock()
    run = True

    # start new game
    game = NewGame()
    clicked = False                # 1 if mouse is clicked and action is pending

    while run:
        clock.tick(FPS)

        # check for events: quit and mouse click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
            # save mouse click location
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True
                    mouse_pos = event.pos
        
        # if click is valid, update board
        if clicked and check_click(game, mouse_pos) >= 0:           # if clicked & click is an actual square
            selected_square = check_click(game, mouse_pos)
            if game.check_available(selected_square):           # check if sqaure is free
                game.make_move(selected_square)
        
        draw_window(game)

        # check win
        if game.check_win()[0]:            # if game is not incomplete
            loser, lose_type = game.check_win()[0], game.check_win()[1]          # save winner and what type of win
            handle_win(game, lose_type)
            handle_message(loser)
            run = False
    run_game()

if __name__ == "__main__":
    run_game()