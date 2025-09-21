import pygame
import sys
import numpy as np

pygame.init()
RESOLUTION = (640, 480)
screen = pygame.display.set_mode(RESOLUTION)

cell_size = 100
board = np.zeros((4, 4), dtype=np.int8)
rows = 4
cols = 4
cell_border = 2
x = int(RESOLUTION[0] / 2 - (cols / 2 * cell_size))
y = int(RESOLUTION[1] / 2 - (rows / 2 * cell_size))
colors = {1: (255, 0, 0), 2: (0, 0, 255)}

selected_cells = 0
mouse_down = False
good_piece = False
player = 1


def draw_board():
    for row in range(rows):
        for col in range(cols):
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (
                    x + col * cell_size,
                    y + row * cell_size,
                    cell_size,
                    cell_size,
                ),
                cell_border,
            )

            if board[row, col] != 0:
                pygame.draw.rect(
                    screen,
                    colors[board[row, col]],
                    (
                        x + col * cell_size + cell_border,
                        y + row * cell_size + cell_border,
                        cell_size - cell_border * 2,
                        cell_size - cell_border * 2,
                    ),
                )


def find_L():
    for row in range(rows - 1):
        for col in range(2):
            if (
                (
                    board[0 + row, 0 + col] == player
                    and board[0 + row, 1 + col] == player
                    and board[0 + row, 2 + col] == player
                    and board[1 + row, 0 + col] == player
                )
                or (
                    board[0 + row, 0 + col] == player
                    and board[1 + row, 0 + col] == player
                    and board[1 + row, 1 + col] == player
                    and board[1 + row, 2 + col] == player
                )
                or (
                    board[1 + row, 0 + col] == player
                    and board[1 + row, 1 + col] == player
                    and board[1 + row, 2 + col] == player
                    and board[0 + row, 2 + col] == player
                )
                or (
                    board[0 + row, 0 + col] == player
                    and board[0 + row, 1 + col] == player
                    and board[0 + row, 2 + col] == player
                    and board[1 + row, 2 + col]
                )
            ):
                return True

    for row in range(2):
        for col in range(cols - 1):
            if (
                (
                    board[0 + row, 0 + col] == player
                    and board[1 + row, 0 + col] == player
                    and board[2 + row, 0 + col] == player
                    and board[2 + row, 1 + col] == player
                )
                or (
                    board[0 + row, 1 + col] == player
                    and board[1 + row, 1 + col] == player
                    and board[2 + row, 1 + col] == player
                    and board[2 + row, 0 + col] == player
                )
                or (
                    board[0 + row, 1 + col] == player
                    and board[0 + row, 0 + col] == player
                    and board[1 + row, 0 + col] == player
                    and board[2 + row, 0 + col] == player
                )
                or (
                    board[0 + row, 0 + col] == player
                    and board[0 + row, 1 + col] == player
                    and board[1 + row, 1 + col] == player
                    and board[2 + row, 1 + col] == player
                )
            ):
                return True


def clear_board():
    global good_piece, selected_cells, board

    good_piece = False
    selected_cells = 0
    board[board == player] = 0


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_q
        ):
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_down = True
            if event.button == 3 and good_piece:
                if player == 1:
                    player = 2
                else:
                    player = 1

                clear_board()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if selected_cells != 4:
                    clear_board()
                else:
                    if find_L():
                        good_piece = True
                    else:
                        clear_board()

                mouse_down = False

    if mouse_down:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_col = (mouse_x - x) // cell_size
        mouse_row = (mouse_y - y) // cell_size

        if mouse_col >= 0 and mouse_col < cols and mouse_row >= 0 and mouse_row < rows:
            if good_piece:
                clear_board()

            elif selected_cells < 4 and board[mouse_row, mouse_col] == 0:
                board[mouse_row, mouse_col] = player
                selected_cells += 1

    screen.fill((255, 255, 255))

    draw_board()

    pygame.display.flip()
