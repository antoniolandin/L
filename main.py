import pygame
import sys
import numpy as np
import ptext

pygame.init()
RESOLUTION = (640, 480)
screen = pygame.display.set_mode(RESOLUTION)
font = pygame.font.Font(None, 100)

cell_size = 100

board = np.array(
    [[3, 1, 1, 0], [0, 2, 1, 0], [0, 2, 1, 0], [0, 2, 2, 3]], dtype=np.int8
)

# last player pieces expressed in (row, col)
last_piece_p1 = [(0, 1), (0, 2), (1, 2), (2, 2)]
last_piece_p2 = [(1, 1), (2, 1), (3, 1), (3, 2)]

board_rows = 4
board_cols = 4
cell_border = 4
x = int(RESOLUTION[0] / 2 - (board_cols / 2 * cell_size - cell_border / 2))
y = int(RESOLUTION[1] / 2 - (board_rows / 2 * cell_size - cell_border / 2))
colors = {1: (255, 0, 0), 2: (0, 0, 255)}

selected_cells = 0
mouse_down = False
good_piece = True
playing = False
turn = 0
winner = None
player = 1
holding_neutral_piece = False
selected_neutral_piece = None

empty_board_surface = pygame.Surface((board_rows * cell_size, board_cols * cell_size))
empty_board_surface.fill((255, 255, 255))

for row in range(board_rows):
    for col in range(board_cols):
        pos_x = col * cell_size
        pos_y = row * cell_size
        border = cell_border

        pygame.draw.rect(
            empty_board_surface,
            (0, 0, 0),
            (
                pos_x - cell_border * col,
                pos_y - cell_border * row,
                cell_size,
                cell_size,
            ),
            border,
        )


def get_last_piece():
    rows, cols = np.where(board == player)
    cells = list(zip(rows, cols))

    return cells


def check_change():
    if player == 1:
        last_piece = last_piece_p1
    else:
        last_piece = last_piece_p2

    change = False
    for cell in last_piece:
        if board[cell] != player:
            change = True

    return change


def draw_board():
    screen.blit(empty_board_surface, (x, y))

    for row in range(board_rows):
        for col in range(board_cols):

            if board[row, col] == 1 or board[row, col] == 2:
                pos_x = x + col * cell_size + cell_border - cell_border * col
                pos_y = y + row * cell_size + cell_border - cell_border * row
                tam_x = cell_size - cell_border * 2
                tam_y = cell_size - cell_border * 2

                if board[row, col] != player or good_piece:
                    if row - 1 >= 0 and board[row - 1, col] == board[row, col]:
                        pos_y -= cell_border * 2
                        tam_y += cell_border * 2
                    else:
                        if col - 1 >= 0 and board[row, col - 1] == board[row, col]:
                            pos_x -= cell_border * 2
                            tam_x += cell_border * 2
                        if (
                            col + 1 < board_cols
                            and board[row, col + 1] == board[row, col]
                        ):
                            tam_x += cell_border

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
                center_y = y + row * cell_size - cell_border * row + radius
                color = (0, 0, 0)

                if selected_neutral_piece and (row, col) == selected_neutral_piece:
                    color = (50, 50, 50)

                pygame.draw.aacircle(
                    screen, color, (center_x, center_y), radius - cell_border
                )


def count_L(cell_type, board):
    possible_L = 0

    for row in range(board_rows - 1):
        for col in range(2):
            if (
                (
                    board[0 + row, 0 + col] == cell_type
                    and board[0 + row, 1 + col] == cell_type
                    and board[0 + row, 2 + col] == cell_type
                    and board[1 + row, 0 + col] == cell_type
                )
                or (
                    board[0 + row, 0 + col] == cell_type
                    and board[1 + row, 0 + col] == cell_type
                    and board[1 + row, 1 + col] == cell_type
                    and board[1 + row, 2 + col] == cell_type
                )
                or (
                    board[1 + row, 0 + col] == cell_type
                    and board[1 + row, 1 + col] == cell_type
                    and board[1 + row, 2 + col] == cell_type
                    and board[0 + row, 2 + col] == cell_type
                )
                or (
                    board[0 + row, 0 + col] == cell_type
                    and board[0 + row, 1 + col] == cell_type
                    and board[0 + row, 2 + col] == cell_type
                    and board[1 + row, 2 + col] == cell_type
                )
            ):
                possible_L += 1

    for row in range(2):
        for col in range(board_cols - 1):
            if (
                (
                    board[0 + row, 0 + col] == cell_type
                    and board[1 + row, 0 + col] == cell_type
                    and board[2 + row, 0 + col] == cell_type
                    and board[2 + row, 1 + col] == cell_type
                )
                or (
                    board[0 + row, 1 + col] == cell_type
                    and board[1 + row, 1 + col] == cell_type
                    and board[2 + row, 1 + col] == cell_type
                    and board[2 + row, 0 + col] == cell_type
                )
                or (
                    board[0 + row, 1 + col] == cell_type
                    and board[0 + row, 0 + col] == cell_type
                    and board[1 + row, 0 + col] == cell_type
                    and board[2 + row, 0 + col] == cell_type
                )
                or (
                    board[0 + row, 0 + col] == cell_type
                    and board[0 + row, 1 + col] == cell_type
                    and board[1 + row, 1 + col] == cell_type
                    and board[2 + row, 1 + col] == cell_type
                )
            ):
                possible_L += 1

    return possible_L


def clear_board():
    global good_piece, selected_cells, board

    good_piece = False
    selected_cells = 0
    board[board == player] = 0


def change_player():
    global winner, player, last_piece_p1, last_piece_p2, turn, playing

    turn += 1

    if player == 1:
        last_piece_p1 = get_last_piece()
        player = 2
    else:
        last_piece_p2 = get_last_piece()
        player = 1

    copy_board = board.copy()
    copy_board[copy_board == player] = 0

    print(f"Possible player's {player} moves: {count_L(0, copy_board) - 1}")

    if count_L(0, copy_board) == 1:
        if player == 1:
            winner = "Blue"
        else:
            winner = "Red"

        playing = False
    else:
        clear_board()


while True:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_col = (mouse_x - x) // cell_size
    mouse_row = (mouse_y - y) // cell_size

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_q
        ):
            pygame.quit()
            sys.exit()

        if playing:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_down = True

                    if (
                        good_piece
                        and mouse_col >= 0
                        and mouse_col < board_cols
                        and mouse_row >= 0
                        and mouse_row < board_rows
                        and board[mouse_row, mouse_col] == 3
                        and not holding_neutral_piece
                    ):
                        holding_neutral_piece = True
                        selected_neutral_piece = (mouse_row, mouse_col)

                if event.button == 3 and good_piece:
                    change_player()

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if holding_neutral_piece:
                        holding_neutral_piece = False

                        if (
                            mouse_col >= 0
                            and mouse_col < board_cols
                            and mouse_row >= 0
                            and mouse_row < board_rows
                            and board[mouse_row, mouse_col] == 0
                        ):
                            board[selected_neutral_piece] = 0
                            board[mouse_row, mouse_col] = 3
                            change_player()

                        selected_neutral_piece = None

                    elif selected_cells != 4:
                        clear_board()
                    else:
                        if count_L(player, board) > 0 and check_change():
                            good_piece = True
                        else:
                            clear_board()

                    mouse_down = False
        else:
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and mouse_col >= 0
                and mouse_col < board_cols
                and mouse_row >= 0
                and mouse_row < board_rows
                and turn == 0
            ):
                playing = True
                clear_board()

    if mouse_down and playing and not holding_neutral_piece:
        if (
            mouse_col >= 0
            and mouse_col < board_cols
            and mouse_row >= 0
            and mouse_row < board_rows
        ):
            if good_piece:
                if board[mouse_row, mouse_col] != 3:
                    clear_board()

            elif selected_cells < 4 and board[mouse_row, mouse_col] == 0:
                board[mouse_row, mouse_col] = player
                selected_cells += 1

    screen.fill((255, 255, 255))

    draw_board()

    if holding_neutral_piece:
        pygame.draw.aacircle(
            screen, (0, 0, 0), (mouse_x, mouse_y), int(cell_size / 2) - cell_border
        )

    if not playing and turn > 0:
        ptext.draw(
            f"{winner} wins",
            owidth=1.5,
            ocolor=(0, 0, 0),
            color=(255, 255, 255),
            center=(int(RESOLUTION[0] / 2), int(RESOLUTION[1] / 2)),
            fontsize=100,
        )

    pygame.display.flip()
