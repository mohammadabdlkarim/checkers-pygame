import pygame
from .constants import WIDTH, HEIGHT, LIGHT_BROWN, DARK_BROWN, GREY, GREEN, BLACK, WHITE, COLS, ROWS, BOX_SIZE
from .Piece import Piece

class Board:
    def __init__(self):
        self._init()
    
    def _init(self):
        self.board = self._create_board()
        self.white_left = self.black_left = 16
        self.white_pieces = self._get_white_pieces(self.board)
        self.black_pieces = self._get_black_pieces(self.board)
    
    def reset(self):
        self._init()
    
    def _create_board(self):
        board = []
        for row in range(ROWS):
            board.append([])
            for col in range(COLS):
                if row < 3 and row > 0:
                    board[row].append(Piece(row, col, BLACK))
                elif row > 4 and row < ROWS - 1:
                    board[row].append(Piece(row, col, WHITE))
                else:
                    board[row].append(0)
        return board
    
    def _get_white_pieces(self, board):
        white_pieces = []
        for row in range(ROWS):
            for piece in board[row]:
                if piece:
                    if piece.color == WHITE:
                        white_pieces.append(piece)
        return white_pieces
            
    def _get_black_pieces(self, board):
        black_pieces = []
        for row in range(ROWS):
            for piece in board[row]:
                if piece:
                    if piece.color == BLACK:
                        black_pieces.append(piece)
        return black_pieces
    
    def move(self, piece, row, col):
        self.board[row][col], self.board[piece.row][piece.col] = self.board[piece.row][piece.col], self.board[row][col]
        piece.move(row, col)
        if row == 0 or row == ROWS - 1:
            piece.make_king()
    
    def check_taken(self, new_piece_row, new_piece_col, piece):
        old_row = piece.row
        old_col = piece.col
        if new_piece_row > old_row + 1: # piece took piece down
            for r in range(old_row + 1, new_piece_row):
                if self.board[r][new_piece_col] != 0:
                    return self.board[r][new_piece_col]
        if new_piece_row < old_row - 1:  # piece took piece up
            for r in range(new_piece_row, old_row):
                if self.board[r][new_piece_col] != 0:
                    return self.board[r][new_piece_col]
        if new_piece_col > old_col + 1:  # piece took piece right
            for c in range(old_col + 1, new_piece_col):
                if self.board[new_piece_row][c] != 0:
                    return self.board[new_piece_row][c]
        if new_piece_col < old_col - 1: # piece took piece left
            for c in range(new_piece_col, old_col):
                if self.board[new_piece_row][c] != 0:
                    return self.board[new_piece_row][c]
        return None

    def get_piece(self, row, col):
        return self.board[row][col]

    def remove(self, piece):
        self.board[piece.row][piece.col] = 0
        if piece.color == BLACK:
            self.black_left -= 1
            self.black_pieces.remove(piece)
        else:
            self.white_left -= 1
            self.white_pieces.remove(piece)
    
    def get_valid_moves(self, piece):
        moves = []
        row = piece.row
        col = piece.col
        if piece != 0:
            # check can take any piece
            can_take = self.can_take_any(piece)
            if can_take:
                for piece_pos in can_take:
                    moves.append(piece_pos)
            else:
                moves = self.check_normal_movement(piece)
            
        return moves

    def check_normal_movement(self, piece):
        moves = []
        row = piece.row
        col = piece.col
        if not piece.king:
            # check moving right
            if not col + 1 >= COLS and self.board[row][col + 1] == 0:
                moves.append((row, col + 1))
            # check moving left
            if not col - 1 < 0 and self.board[row][col - 1] == 0:
                moves.append((row, col - 1))
            # check moving up
            if piece.color == WHITE:
                if not row - 1 < 0 and self.board[row - 1][col] == 0:
                    moves.append((row - 1, col))
            # check moving down
            if piece.color == BLACK:
                if not row + 1 >= ROWS and self.board[row + 1][col] == 0:
                    moves.append((row + 1, col))
        
        else:
            # check moving right
            for c in range(col + 1, COLS):
                if self.board[row][c] != 0:
                    break
                else:
                    moves.append((row, c))
            # check moving left
            for c in range(col - 1, -1, -1):
                if self.board[row][c] != 0:
                    break
                else:
                    moves.append((row, c))
            # check moving up
            for r in range(row - 1, -1, -1):
                if self.board[r][col] != 0:
                    break
                else:
                    moves.append((r, col))
            # check moving down
            for r in range(row + 1, ROWS):
                if self.board[r][col] != 0:
                    break
                else:
                    moves.append((r, col))

        return moves

    def can_take_any(self, piece):
        if piece != 0:
            can_take_pieces = []
            if piece.king:
                last_top_row = 0
                last_bottom_row = ROWS - 1
                last_right_col = COLS - 1
                last_left_col = 0
            else:
                last_right_col = piece.col + 2
                last_left_col = piece.col - 2
                last_top_row = piece.row - 2
                last_bottom_row = piece.row + 2

            # check can take in same col down
            if last_bottom_row <= ROWS - 1:
                if piece.color == BLACK or piece.king:
                    for r in range(piece.row, last_bottom_row):
                        if self.can_take_piece(piece, self.board[r][piece.col]):
                            if self.board[r + 1][piece.col] == 0:
                                can_take_pieces.append((r + 1, piece.col))
                                row_down = r + 1

                                while row_down <= last_bottom_row:
                                    if self.board[row_down][piece.col] != 0:
                                        break

                                    can_take_pieces.append((row_down, piece.col))
                                    row_down += 1
                                    
                                if row_down <=  last_bottom_row and self.board[row_down][piece.col] != 0:
                                    break

                            else:
                                break
            # check can take in same col up
            if last_top_row >= 0:
                if piece.color == WHITE or piece.king:
                    for r in range(piece.row - 1, last_top_row, -1):
                        if self.can_take_piece(piece, self.board[r][piece.col]):
                            if self.board[r - 1][piece.col] == 0:
                                can_take_pieces.append((r - 1, piece.col))
                                row_up = r - 1

                                while row_up >= last_top_row:
                                    if self.board[row_up][piece.col] != 0:
                                        break

                                    can_take_pieces.append((row_up, piece.col))
                                    row_up -= 1
                                
                                if row_up >= last_top_row and self.board[row_up][piece.col] != 0:
                                    break

                            else:
                                break

            # check can take in same row right
            if last_right_col <= COLS - 1:
                for c in range(piece.col, last_right_col):
                    if self.can_take_piece(piece, self.board[piece.row][c]):
                        if self.board[piece.row][c + 1] == 0:
                            can_take_pieces.append((piece.row, c + 1))
                            col_right = c + 1

                            while col_right <= last_right_col:
                                if self.board[piece.row][col_right] != 0:
                                    break

                                can_take_pieces.append((piece.row, col_right))
                                col_right += 1

                            if col_right <= last_right_col and self.board[piece.row][col_right] != 0:
                                break
                                
                        else:
                            break
                        
            # check can take in same row left
            if last_left_col >= 0:
                for c in range(piece.col-1, last_left_col, -1):
                    if self.can_take_piece(piece, self.board[piece.row][c]):
                        if self.board[piece.row][c - 1] == 0:
                            can_take_pieces.append((piece.row, c - 1))
                            col_left = c - 1

                            while col_left >= last_left_col:
                                if self.board[piece.row][col_left] != 0:
                                    break
                                can_take_pieces.append((piece.row, col_left))
                                col_left -= 1
                            
                            if col_left >= last_left_col and self.board[piece.row][col_left] != 0:
                                break

                        else:
                            break

            return can_take_pieces

    def can_take_piece(self, piece, to_take):
        if piece != 0 and to_take != 0 and piece.color != to_take.color:
            return to_take
    
    def winner(self):
        if self.black_left == 0:
            return WHITE
        elif self.white_left == 0:
            return BLACK
        
    def draw_board(self, win):
        win.fill(LIGHT_BROWN)
        for row in range(ROWS):
            for col in range(row%2, COLS, 2):
                pygame.draw.rect(win, DARK_BROWN, (BOX_SIZE * col, BOX_SIZE * row, BOX_SIZE, BOX_SIZE))
                
    def draw_pieces(self, win):
        for row in range(len(self.board)):
            for piece in self.board[row]:
                if piece != 0:
                    piece.draw(win)
    
    def draw_valid_moves(self, win, piece, moves):
        color = GREY
        if self.can_take_any(piece):
            color = GREEN
        for move in moves:
            pygame.draw.circle(win, color, (move[1]*BOX_SIZE + BOX_SIZE // 2, move[0]*BOX_SIZE + BOX_SIZE // 2), 10)
    
    def draw_window(self, win):
        self.draw_board(win)
        self.draw_pieces(win)

    