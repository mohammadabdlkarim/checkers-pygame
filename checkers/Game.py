import pygame
from .constants import WHITE, BLACK, winner_font, WIDTH, HEIGHT

class Game:
    def __init__(self, board):
        self._init(board)

    def _init(self, board):
        self.board = board
        self.selected = None
        self.turn = WHITE
        self.last_played = BLACK
        self.last_piece_moved = None
        self.valid_moves = {}
    
    def reset(self, board):
        self.board.reset()
        self._init(board)

    def select(self, row, col):
        if self.last_played == self.turn:
            self.selected = self.last_piece_moved
        piece = self.board.get_piece(row, col)
        if self.selected:
            taken = self.board.check_taken(row, col, self.selected)
            result = self.move(self.selected, row, col)
            if not result and self.turn != self.last_played:
                if piece != 0 and piece.color == self.turn:
                    self.selected = None
                    self.select(row, col)
            else:
                if taken:
                    self.last_played = self.turn
                    self.board.remove(taken)
                    if not self.board.can_take_any(self.selected):
                        self.selected = None
                        self.change_turn()
                    else:
                        self.selected = self.last_piece_moved
                        self.valid_moves = self.board.get_valid_moves(self.selected)

        if piece != 0 and piece.color == self.turn and self.last_played != self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
    
    def move(self, piece, row, col):
        if (row, col) in self.valid_moves:
            taken = self.board.check_taken(row, col, piece)
            self.board.move(piece, row, col)
            self.last_piece_moved = piece
            if not taken:
                self.selected = None
                self.change_turn()
            return True
        return False
    
    def change_turn(self):
        self.last_played = self.turn
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE
    
    def draw_winner(self, win):
        if self.board.winner():
            if self.board.winner() == BLACK:
                winner_label = winner_font.render('Player Two Wins', True, BLACK)
            else:
                winner_label = winner_font.render('Player One Wins', True, BLACK)
            win.blit(winner_label, (WIDTH // 2 - winner_label.get_width() // 2, HEIGHT // 2 - winner_label.get_height()))
            play_again_label = winner_font.render('Press Space Button To Play Again', True, BLACK)
            win.blit(play_again_label, (WIDTH // 2 - play_again_label.get_width() // 2, HEIGHT // 2 + winner_label.get_height()))

    def draw_selected(self, win):
        if self.selected:
            if self.selected.color == WHITE:
                pygame.draw.circle(win, BLACK, (self.selected.x, self.selected.y),  10)
            else:
                pygame.draw.circle(win, WHITE, (self.selected.x, self.selected.y), 10)
            if self.valid_moves:
                self.board.draw_valid_moves(win, self.selected, self.valid_moves)
    
    def draw_window(self, win):
        self.board.draw_window(win)
        self.draw_winner(win)
        self.draw_selected(win)