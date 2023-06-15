import pygame
import os
import random
from typing import List, Optional
pygame.font.init()          # initialize font library
pygame.mixer.init()         # pygame sound

from game_logic import *

# window size = (320 x 320) + (15 x 15 border on each edge)
# each square is (100 x 100), with 10 x 10 lines
WIDTH, HEIGHT = 350, 350

# set display and caption
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reverse TicTacToe")

# colors rgb
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (70, 70, 70)

# game colors
BACKGROUND_COLOR = WHITE
LINE_COLOR = GRAY
TICK_COLOR = BLACK
BORDER_COLOR = GRAY
CROSS_COLOR = GRAY

# fonts for displaying winner
CAPTION_FONT = pygame.font.SysFont('avenir', 12)

# basic settings
FPS = 60        # frame rate
LINE_THICKNESS = 10             # line to divide squares
LINE_LENGTH = 350
CROSS_THICKNESS = 10             # for crossing out a win
SHORT_CROSS_LENGTH = 250
LONG_CROSS_LENGTH = 350         ## FIX
SQUARE_SIZE = 100
BORDER_SIZE = 15
TICK_WIDTH = 100            # ticks: O and X
TICK_HEIGHT = 100

# define borders
TOP_SIDE = pygame.Rect(0, 0, WIDTH, BORDER_SIZE)
BOTTOM_SIDE = pygame.Rect(0, HEIGHT - BORDER_SIZE, WIDTH, BORDER_SIZE)
LEFT_SIDE = pygame.Rect(0, 0, BORDER_SIZE, HEIGHT)
RIGHT_SIDE = pygame.Rect(WIDTH - BORDER_SIZE, 0, BORDER_SIZE, HEIGHT)
BORDERS = [TOP_SIDE, BOTTOM_SIDE, LEFT_SIDE, RIGHT_SIDE]

# define lines (lines go beneath border)
HORI_LINE_1 = pygame.Rect(
    0, BORDER_SIZE + SQUARE_SIZE, LINE_LENGTH, LINE_THICKNESS)
HORI_LINE_2 = pygame.Rect(
    0, BORDER_SIZE + LINE_THICKNESS + 2*SQUARE_SIZE, LINE_LENGTH, LINE_THICKNESS)
VERT_LINE_1 = pygame.Rect(
    BORDER_SIZE + SQUARE_SIZE, 0, LINE_THICKNESS, LINE_LENGTH)
VERT_LINE_2 = pygame.Rect(
    BORDER_SIZE + LINE_THICKNESS + 2*SQUARE_SIZE, 0, LINE_THICKNESS, LINE_LENGTH)
LINES = (HORI_LINE_1, HORI_LINE_2, VERT_LINE_1, VERT_LINE_2)

# define cross lines
SHORT_CROSS_RECT = pygame.Rect(0, 0, SHORT_CROSS_LENGTH, CROSS_THICKNESS)       # create rect
LONG_CROSS_RECT = pygame.Rect(0, 0, LONG_CROSS_LENGTH, CROSS_THICKNESS)
SHORT_CROSS = pygame.Surface((SHORT_CROSS_RECT.width, SHORT_CROSS_RECT.height))     # create surf to rotate
LONG_CROSS = pygame.Surface((LONG_CROSS_RECT.width, LONG_CROSS_RECT.height), pygame.SRCALPHA)
pygame.draw.rect(SHORT_CROSS, CROSS_COLOR, SHORT_CROSS_RECT)           # draw rect onto surf
pygame.draw.rect(LONG_CROSS, CROSS_COLOR, LONG_CROSS_RECT)
HORI_CROSS = SHORT_CROSS
VERT_CROSS = pygame.transform.rotate(SHORT_CROSS, 90)
DIAG_DOWN_CROSS = pygame.transform.rotate(LONG_CROSS, -45)
DIAG_UP_CROSS = pygame.transform.rotate(LONG_CROSS, 45)


# defining center coordinates of squares
UNIT = SQUARE_SIZE + LINE_THICKNESS
CENTER_X, CENTER_Y = WIDTH//2, HEIGHT//2
SQUARE_0 = (CENTER_X - UNIT, CENTER_Y - UNIT)
SQUARE_1 = (CENTER_X, CENTER_Y - UNIT)
SQUARE_2 = (CENTER_X + UNIT, CENTER_Y - UNIT)
SQUARE_3 = (CENTER_X - UNIT, CENTER_Y)
SQUARE_4 = (CENTER_X, CENTER_Y)
SQUARE_5 = (CENTER_X + UNIT, CENTER_Y)
SQUARE_6 = (CENTER_X - UNIT, CENTER_Y + UNIT)
SQUARE_7 = (CENTER_X, CENTER_Y + UNIT)
SQUARE_8 = (CENTER_X + UNIT, CENTER_Y + UNIT)
SQUARES = (SQUARE_0, SQUARE_1, SQUARE_2, SQUARE_3, SQUARE_4, SQUARE_5, SQUARE_6, SQUARE_7, SQUARE_8)

# ticks
O = pygame.image.load(
    os.path.join('assets', 'O.png'))
O = pygame.transform.scale(
    O, (TICK_WIDTH, TICK_HEIGHT))

X = pygame.image.load(
    os.path.join('assets', 'X.png'))
X = pygame.transform.scale(
    X, (TICK_WIDTH, TICK_HEIGHT))

# EVENTS
# event1: game ends
GAME_ENDS = pygame.USEREVENT + 1

# FUNCTIONS
def draw_window(game: NewGame):
    # fill BG
    WIN.fill(BACKGROUND_COLOR)
    
    # draw lines
    for line in LINES:
        pygame.draw.rect(WIN, LINE_COLOR, line)

    # draw borders
    for border in BORDERS:
        pygame.draw.rect(WIN, BORDER_COLOR, border)

    # draw ticks
    for i in range(3):      # rows
        for j in range(3):      # cols
            square_no = 3*i + j     # check all squares with this method

            if game.board[i][j] == 1:           # if tick is O
                O_rect = O.get_rect()           # get the rectangle of surface O
                O_rect.center = SQUARES[square_no]      # set center according to square no.
                WIN.blit(O, O_rect)
            elif game.board[i][j] == 2:         # if tick is X
                X_rect = X.get_rect()           # get the rectangle of surface X
                X_rect.center = SQUARES[square_no]      # set center according to square no.
                WIN.blit(X, X_rect)

    # display
    pygame.display.update()

def handle_win(game, lose_type):
    if lose_type == -1:          # game is a draw
        return

    # n-th win type corresponds to the type of cross
    cross_type_per_lose_type = (HORI_CROSS, HORI_CROSS, HORI_CROSS, VERT_CROSS, VERT_CROSS, VERT_CROSS, DIAG_DOWN_CROSS, DIAG_UP_CROSS)

    # n-th win type corresponds to the center square
    center_square_per_lose_type = (1, 4, 7, 3, 4, 5, 4, 4)

    # use above info to find cross and center_square
    cross, center_square = cross_type_per_lose_type[lose_type], center_square_per_lose_type[lose_type]
    center_coord = SQUARES[center_square]   # center coordinates according to center square

    cross_rect = cross.get_rect()
    cross_rect.center = center_coord

    WIN.blit(cross, cross_rect)     # display cross
    pygame.display.update()

def handle_message(loser):
    if loser == -1:
        print("Game ends in a draw.")
    else:
        print(f"Game over. Player {loser} loses!")
    pygame.time.delay(3000)

def check_click(game: NewGame, mouse_pos: tuple or None) -> int:
    """Given board state and mouse position when mouse is clicked:\n
    return -1 if click is out of bounds or invalid\n
    else return selected square number (0-8)"""

    if mouse_pos == None:
        return -1

    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]

    for square_no, square_center_coordinates in enumerate(SQUARES):
        square_x, square_y = square_center_coordinates[0], square_center_coordinates[1]
        half_unit = SQUARE_SIZE//2

        if mouse_x in range(
            square_x - half_unit, square_x + half_unit) and mouse_y in range(square_y - half_unit, square_y + half_unit):
            return square_no
    
    # no squares were clicked
    return -1
