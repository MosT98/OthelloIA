import pygame as pg

ROWS = 8
COLUMNS = 8
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BACKGROUND = (0, 204, 153)
WHITE = (255, 255, 255)

PIECE_SIZE = 100
BOARD_WIDTH = PIECE_SIZE * COLUMNS
BOARD_HEIGHT = PIECE_SIZE * ROWS
BOARD_SIZE = (BOARD_WIDTH, BOARD_HEIGHT)
RADIUS = int(PIECE_SIZE / 2 - 5)
screen = pg.display.set_mode(BOARD_SIZE)
pg.display.set_caption('Othello')


def draw_board(board):
    for c in range(COLUMNS):
        for r in range(ROWS):
            pg.draw.rect(screen, BACKGROUND, (c * PIECE_SIZE, r * PIECE_SIZE, PIECE_SIZE, PIECE_SIZE))
            pg.draw.circle(screen, BACKGROUND,
                           (int(c * PIECE_SIZE + PIECE_SIZE / 2), int(r * PIECE_SIZE + PIECE_SIZE / 2)),
                           RADIUS)

    for c in range(COLUMNS):
        for r in range(ROWS):
            if board[r][c] == 2:
                pg.draw.circle(screen, BLACK, (int(c * PIECE_SIZE + PIECE_SIZE / 2),
                                               BOARD_HEIGHT - int(r * PIECE_SIZE + PIECE_SIZE / 2)), RADIUS)
            elif board[r][c] == 1:
                pg.draw.circle(screen, WHITE, (int(c * PIECE_SIZE + PIECE_SIZE / 2),
                                               BOARD_HEIGHT - int(r * PIECE_SIZE + PIECE_SIZE / 2)), RADIUS)
    pg.display.update()


def draw_background():
    for c in range(COLUMNS):
        for r in range(ROWS):
            pg.draw.rect(screen, BACKGROUND, (c * PIECE_SIZE, r * PIECE_SIZE, PIECE_SIZE, PIECE_SIZE))


def get_mouse_position():
    (mouse_x, mouse_y) = pg.mouse.get_pos()
    position = (mouse_x // PIECE_SIZE), (mouse_y // PIECE_SIZE)
    position = (position[1], position[0])
    print(position)
    return position


def drawing_pieces(board, piece):
    if piece == 1:
        COLOR = BLACK
    elif piece == 2:
        COLOR = WHITE

    for row in range(8):
        for column in range(8):
            if board[row][column] == piece:
                pg.draw.circle(screen, COLOR, (
                    column * 100 + PIECE_SIZE // 2, row * 100 + PIECE_SIZE // 2), RADIUS)
                pg.display.update()


def drawing_possible_moves_for_player(board, piece):
    for row in range(8):
        for column in range(8):
            if board[row][column] == piece:
                pg.draw.circle(screen, BLACK, (
                    column * 100 + PIECE_SIZE // 2, row * 100 + PIECE_SIZE // 2), RADIUS, 1)
            pg.display.update()


def checking_possible_moves(moves):
    for move in moves:
        for i in move:
            pg.draw.circle(screen, BACKGROUND, (
                i[1] * 100 + PIECE_SIZE // 2, i[0] * 100 + PIECE_SIZE // 2), RADIUS+1)
        pg.display.update()
