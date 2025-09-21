import pygame
import sys
import numpy as np

pygame.init()
RESOLUTION = (640, 480)
screen = pygame.display.set_mode(RESOLUTION)

cell_size = 100

board = np.array(
    [[3, 1, 1, 0], [0, 2, 1, 0], [0, 2, 1, 0], [0, 2, 2, 3]], dtype=np.int8
)

rows = 4
cols = 4
cell_border = 4
x = int(RESOLUTION[0] / 2 - (cols / 2 * cell_size - cell_border / 2))
y = int(RESOLUTION[1] / 2 - (rows / 2 * cell_size - cell_border / 2))
colors = {1: (255, 0, 0), 2: (0, 0, 255)}

selected_cells = 0
mouse_down = False
good_piece = True
player = 1


def draw_board():
    for row in range(rows):
        for col in range(cols):
            pos_x = x + col * cell_size
            pos_y = y + row * cell_size
            border = cell_border

            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (
                    pos_x - cell_border * col,
                    pos_y - cell_border * row,
                    cell_size,
                    cell_size,
                ),
                border,
            )

            if board[row, col] == 1 or board[row, col] == 2:
                pos_x = x + col * cell_size + cell_border - cell_border * col
                pos_y = y + row * cell_size + cell_border - cell_border * row
                tam_x = cell_size - cell_border * 2
                tam_y = cell_size - cell_border * 2

                if board[row, col] != player or good_piece:
                    if row - 1 >= 0 and board[row - 1, col] == board[row, col]:
                        pos_y -= cell_border * 2
                        tam_y += cell_border * 2
                    if col - 1 >= 0 and board[row, col - 1] == board[row, col]:
                        pos_x -= cell_border * 2
                        tam_x += cell_border * 2

                pygame.draw.rect(
                    screen,
                    colors[board[row, col]],
                    (
                        pos_x,
                        pos_y,
                        tam_x,
                        tam_y,
                    ),
                )

            elif board[row, col] == 3:
                radius = int(cell_size / 2)
                center_x = x + col * cell_size - cell_border * col + radius
                center_y = y + row * cell_size - cell_border * col + radius

                pygame.draw.aacircle(
                    screen, (0, 0, 0), (center_x, center_y), radius - cell_border
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
