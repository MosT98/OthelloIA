from Heuristic_Evaluation import heuristic_evaluation_function

import numpy as np
import math

computer_piece = 2


def add_piece_to_board(board, row, column, current_piece):
    from Board_Representation import isValidMove

    pieces_to_flip = isValidMove(board, row, column, current_piece)
    if len(pieces_to_flip) > 0:
        board[row][column] = current_piece
        for row, col in pieces_to_flip:
            board[row][col] = current_piece

    return board


def local_maximization(board, piece):
    from Board_Representation import get_moves

    current_value = -math.inf
    current_row = -1
    current_column = -1

    valid_moves = get_moves(board, piece)

    for move in valid_moves:
        board_modified = np.copy(board)
        add_piece_to_board(board_modified, move[0], move[1], piece)
        new_value = heuristic_evaluation_function(board_modified, piece)

        if new_value > current_value:
            current_value = new_value
            current_row = move[0]
            current_column = move[1]

    return (current_row, current_column)
