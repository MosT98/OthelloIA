from Heuristic_Evaluation import heuristic_evaluation_function

import numpy as np
import math

computer_piece = 2


def is_terminal_state(board, current_piece):
    from Board_Representation import get_moves
    if len(get_moves(board, current_piece)) == 0:
        return True
    else:
        return False

def add_piece_to_board(board, row, column, current_piece):
    from Board_Representation import isValidMove

    pieces_to_flip = isValidMove(board, row, column, current_piece)
    if len(pieces_to_flip) > 0:
        board[row][column] = current_piece
        for row, col in pieces_to_flip:
            board[row][col] = current_piece

    return board

def negamax_alg(board, current_piece, color, current_depth, target_depth):
    from Board_Representation import get_moves

    if current_depth == target_depth or is_terminal_state(board, current_piece) == True:
        return (None, None, color * heuristic_evaluation_function(board, computer_piece))

    current_value = -math.inf
    current_row = -1
    current_column = -1

    valid_moves = get_moves(board, current_piece)

    if len(valid_moves) == 0:
        return (None, None, 0)
    else:
        for move in valid_moves:
            board_modified = np.copy(board)
            add_piece_to_board(board_modified, move[0], move[1], current_piece)
            new_row, new_column, new_value = negamax_alg(board_modified, 3 - current_piece, -color,
                                                         current_depth + 1, target_depth)

            if -new_value > current_value:
                current_value = -new_value
                current_row = move[0]
                current_column = move[1]

        return (current_row, current_column, current_value)


def negamax(board, piece, depth):
    best_row, best_column, best_score = negamax_alg(board, current_piece=piece, color=1, current_depth=0,
                                                    target_depth=depth)

    return (best_row, best_column)
