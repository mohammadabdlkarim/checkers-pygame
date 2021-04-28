import pygame
import os
pygame.font.init()

# Sizes
WIDTH, HEIGHT = 600, 600
ROWS = COLS = 8
BOX_SIZE = WIDTH // ROWS
PIECE_PADDING = 15
PIECE_OUTLINE = 2

# Colors
LIGHT_BROWN = 204, 153, 102
DARK_BROWN = 255, 242, 230
GREY = 153, 153, 102
BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0

# Images
CROWN_IMAGE = pygame.image.load(os.path.join('checkers/assets', 'crown.png'))
CROWN = pygame.transform.scale(CROWN_IMAGE, (35, 15))

# Fonts
winner_font = pygame.font.SysFont('comicsans', 50)