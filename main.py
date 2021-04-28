import pygame
from checkers.constants import WIDTH, HEIGHT, BOX_SIZE
from checkers.Board import Board
from checkers.Game import Game

pygame.display.set_caption("Checkers")
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

def get_row_col_mouse(pos):
    x, y = pos
    row = y // BOX_SIZE
    col = x // BOX_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    fps = 60
    board = Board()
    game = Game(board)

    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_mouse(pos)
                game.select(row, col)

        game.draw_window(WIN)
        pygame.display.update()


if __name__ == "__main__":
    main()