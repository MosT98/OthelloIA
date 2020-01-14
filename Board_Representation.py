import numpy as np
import pandas as pd

pd.set_option('display.expand_frame_repr', False)

ROWS = 8
COLUMNS = 8
DIRECTIONS = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]  # NV, N, NE, E, V, SV, S, SE


def create_board():
    board = np.zeros((ROWS, COLUMNS), dtype=int)
    board[3][3] = 1
    board[3][4] = 2
    board[4][3] = 2
    board[4][4] = 1
    return board


def show_board(board):
    print(pd.DataFrame(
        data=board, index=["Row 0", "Row 1", "Row 2", "Row 3", "Row 4", "Row 5", "Row 6", "Row 7"],
        columns=["Column 0", "Column 1", "Column 2", "Column 3", "Column 4", "Column 5", "Column 6", "Column 7"]))
    print()


def isValidLocation(board, row, column):
    return board[row][column] == 0


def isOnBoard(row, column):
    return 0 <= row <= 7 and 0 <= column <= 7


def place_piece(board, row, column, piece):
    board[row][column] = piece


def isValidMove(board, row, column, piece):
    if not isValidLocation(board, row, column) or not isOnBoard(row, column):
        return False
    # stim ca este pe board, deci putem pune piesa

    board[row][column] = piece
    other_piece = 0
    if piece == 1:
        other_piece = 2
    else:
        other_piece = 1

    pieces_to_flip = []  # vector pentru a manca mai multe piese

    for x, y in DIRECTIONS:
        row_copy, column_copy = row, column
        row_copy += x
        column_copy += y
        # facem cate un pas in acea directie, apoi verificam
        if isOnBoard(row_copy, column_copy) and board[row_copy][column_copy] == other_piece:
            row_copy += x
            column_copy += y
            if not isOnBoard(row_copy, column_copy):  # schimbam directia daca pozitia nu se afla in board
                continue
            while board[row_copy][column_copy] == other_piece:
                row_copy += x
                column_copy += y
                if not isOnBoard(row_copy, column_copy):
                    break
            if not isOnBoard(row_copy, column_copy):
                continue
            if board[row_copy][column_copy] == piece:
                # daca ajungem ca in pozitia curenta sa fie o piesa de-a noastra, le mancam pe celelalte de pe drum
                while True:
                    row_copy -= x
                    column_copy -= y
                    if row_copy == row and column_copy == column:
                        break
                    pieces_to_flip.append([row_copy, column_copy])
    board[row][column] = 0
    if len(pieces_to_flip) == 0:
        return False

    return pieces_to_flip


def get_moves(board, piece):
    moves = []
    for r in range(ROWS):
        for c in range(COLUMNS):
            if isValidMove(board, r, c, piece) != False:
                moves.append([r, c])
    return moves


def board_with_moves(board, piece):  # e doar de verificare, probabil o s-o stergem mai tarziu
    copy_board = board
    for x, y in get_moves(copy_board, piece):
        copy_board[x][y] = 3
    return copy_board


def corner_move(row, column):
    return (row == 0 and column == 0) or (row == 0 and column == 7) or (row == 7 and column == 0) or (
            row == 7 and column == 7)


def player_move(board, piece):
    while True:
        print("Introduceti mutarea dorita(Player " + str(piece) + "):")
        move = input()
        command = move.split(' ')
        if len(command) == 2:
            print("sal")
            r = int(command[0])
            c = int(command[1])
            print(r)
            print(c)
            if not isValidMove(board, r, c, piece):
                continue
            else:
                break
    return [r, c]


def make_move(board, row, column, piece):
    pieces_to_flip = isValidMove(board, row, column, piece)

    if not pieces_to_flip:
        return False

    board[row][column] = piece
    for r, c in pieces_to_flip:
        board[r][c] = piece
    return True


if __name__ == '__main__':
    board = create_board()
    # b2 = board_with_moves(board, 1)
    # show_board(b2)
    turn = 'p1'
    while True:
        if turn == 'p1':
            show_board(board)
            move = player_move(board, 1)
            make_move(board, move[0], move[1], 1)

            if get_moves(board, 2) == []:
                break
            else:
                turn = 'p2'
        elif turn == 'p2':
            show_board(board)
            move = player_move(board, 2)
            make_move(board, move[0], move[1], 2)

            if get_moves(board, 1) == []:
                break
            else:
                turn = 'p1'

    show_board(board)
