import pygame
from .constants import BOX_SIZE, PIECE_PADDING, PIECE_OUTLINE, GREY, CROWN, WHITE, BLACK


class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = self.y = 0
        self.calculate_pos()

    def calculate_pos(self):
        self.x = self.col * BOX_SIZE + BOX_SIZE // 2
        self.y = self.row * BOX_SIZE + BOX_SIZE // 2

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calculate_pos()

    def make_king(self):
        self.king = True

    def set_row_col(self, row, col):
        self.row = row
        self.col = col
    
    def draw(self, win):
        radius = BOX_SIZE // 2 - PIECE_PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + PIECE_OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))
    
    def __repr__(self):
        return str(self.color)