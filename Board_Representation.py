import copy

from Graphic_Representation import *
from Heuristic_Evaluation import heuristic_evaluation_function
from Local_Maximization import local_maximization
from Alpha_Beta_Pruning import alpha_beta_pruning
from Negamax import negamax
from Quiescence_Search import quiescence_search

import sys
import numpy as np
import pandas as pd
import math

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

    drawing_pieces(board, piece)
    return True


def check_moves(prev_moves, actual_moves):
    to_redraw = []
    if prev_moves not in actual_moves:
        to_redraw.append(prev_moves)

    checking_possible_moves(to_redraw)


def get_scores(board, player_piece, computer_piece):
    player_score = 0
    computer_score = 0
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == player_piece:
                player_score += 1
            elif board[row][col] == computer_piece:
                computer_score += 1

    return player_score, computer_score


def is_board_complete(board):
    counter = 0
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == 0:
                counter += 1
    return counter == 0

if __name__ == '__main__':
    strategy = int(input("Select strategy:"))

    pg.init()
    FONT = pg.font.SysFont('comicsansms', 70)
    board = create_board()
    screen = pg.display.set_mode(BOARD_SIZE)
    draw_board(board)
    pg.display.update()
    show_board(board)
    game_over = False
    turn = 0
    while not game_over:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if turn == 0:
                possible_moves_board = np.zeros((ROWS, COLUMNS), dtype=int)
                moves = get_moves(board, 1)
                copy_moves = copy.deepcopy(moves)

                for move in moves:
                    possible_moves_board[move[0]][move[1]] = 1
                drawing_possible_moves_for_player(possible_moves_board, 1)

                if event.type == pg.MOUSEBUTTONDOWN:
                    print("PLAYER 1")
                    if len(get_moves(board, 1)) != 0:
                        check_moves(copy_moves, moves)
                        position = get_mouse_position()
                        if [position[0], position[1]] not in moves:
                            continue
                        else:
                            make_move(board, position[0], position[1], 1)
                            p_score, c_score = get_scores(board, 1, 2)
                            pg.display.set_caption('[Othello]COMPUTER:' + str(c_score) + ' PLAYER:' + str(p_score))
                    else:
                        print("Player skips this round.")

                    if len(get_moves(board, 2)) == 0:
                        game_over = True
                        winning_text = FONT.render('PLAYER WINS', True, RED)
                        draw_background()
                        screen.blit(winning_text, (100, 350))
                        pg.display.update()
                        break
                    elif is_board_complete(board) == True:
                        game_over = True
                        player_score, computer_score = get_scores(board, 1, 2)
                        if computer_score > player_score:
                            winning_text = FONT.render('COMPUTER WINS', True, RED)
                        elif player_score > computer_score:
                            winning_text = FONT.render('PLAYER WINS', True, RED)
                        else:
                            winning_text = FONT.render('DRAW', True, RED)
                        draw_background()
                        screen.blit(winning_text, (100, 350))
                        pg.display.update()
                        break
                    else:
                        turn += 1

            elif turn == 1:
                print("COMPUTER")
                if len(get_moves(board, 2)) != 0:
                    if strategy == 1:   # Local Maximization
                        row, column = local_maximization(board, 2)
                        print((row, column))
                        if isOnBoard(row, column):
                            if board[row][column] == 0:
                                make_move(board, row, column, 2)
                            p_score, c_score = get_scores(board, 1, 2)
                            pg.display.set_caption('[Othello]COMPUTER:' + str(c_score) + ' PLAYER:' + str(p_score))
                        else:
                            print("Computer skips this round.")

                    elif strategy == 2:  # Alpha Beta Pruning
                        row, column = alpha_beta_pruning(board, 2, 3)
                        print((row, column))
                        if isOnBoard(row, column):
                            if board[row][column] == 0:
                                make_move(board, row, column, 2)
                            p_score, c_score = get_scores(board, 1, 2)
                            pg.display.set_caption('[Othello]COMPUTER:' + str(c_score) + ' PLAYER:' + str(p_score))
                        else:
                           print("Computer skips this round.")

                    elif strategy == 3:  # Negamax
                        row, column = negamax(board, 2, 3)
                        print((row, column))
                        if isOnBoard(row,column):
                            if board[row][column] == 0:
                                make_move(board, row, column, 2)
                            p_score, c_score = get_scores(board, 1, 2)
                            pg.display.set_caption('[Othello]COMPUTER:' + str(c_score) + ' PLAYER:' + str(p_score))
                        else:
                           print("Computer skips this round.")

                    elif strategy == 4:  # Quiescene Search
                        row, column = quiescence_search(board, 2, 3)
                        print((row, column))
                        if isOnBoard(row,column):
                           if board[row][column] == 0:
                                make_move(board, row, column, 2)
                           p_score, c_score = get_scores(board, 1, 2)
                           pg.display.set_caption('[Othello]COMPUTER:' + str(c_score) + ' PLAYER:' + str(p_score))
                        else:
                          print("Computer skips this round.")
                else:
                    print("Computer skips this round.")

                if len(get_moves(board, 1)) == 0:
                    game_over = True
                    winning_text = FONT.render('COMPUTER WINS', True, RED)
                    draw_background()
                    screen.blit(winning_text, (100, 350))
                    pg.display.update()
                    break
                elif is_board_complete(board) == True:
                    game_over = True
                    player_score, computer_score = get_scores(board, 1, 2)
                    if computer_score > player_score:
                        winning_text = FONT.render('COMPUTER WINS', True, RED)
                        print('c wins')
                    elif player_score > computer_score:
                        winning_text = FONT.render('PLAYER WINS', True, RED)
                        print('p wins')
                    else:
                        winning_text = FONT.render('DRAW', True, RED)
                    draw_background()
                    screen.blit(winning_text, (100, 350))
                    pg.display.update()
                    break
                else:
                    turn -= 1

        if game_over == True:
            pg.time.wait(5000)
