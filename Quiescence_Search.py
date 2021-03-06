from Heuristic_Evaluation import heuristic_evaluation_function

import numpy as np
import math

computer_piece = 2

CORNERS_LIST = [(0, 0), (0, 7), (7, 0), (7, 7)]
ADJACENT_CORNERS_LIST = [(0, 2), (1, 1), (1, 0), (0, 6), (1, 6), (1, 7), (6, 0), (6, 1), (7, 1), (7, 6), (6, 6), (6, 7)]


def add_piece_to_board(board, row, column, current_piece):
    from Board_Representation import isValidMove

    pieces_to_flip = isValidMove(board, row, column, current_piece)
    if len(pieces_to_flip) > 0:
        board[row][column] = current_piece
        for row, col in pieces_to_flip:
            board[row][col] = current_piece

    return board


def ordering_moves(board, current_piece, depth):
    from Board_Representation import get_moves

    possible_moves = get_moves(board, current_piece)
    scores_possible_moves = []

    for move in possible_moves:
        board_modified = np.copy(board)
        add_piece_to_board(board_modified, move[0], move[1], current_piece)
        scores_possible_moves.append(heuristic_evaluation_function(board_modified, current_piece))

    possible_moves_sorted = ()
    if depth % 2 == 0:
        possible_moves_sorted, scores_possible_moves_sorted = zip(
            *sorted(zip(possible_moves, scores_possible_moves), reverse=True))
    elif depth % 2 != 0:
        possible_moves_sorted, scores_possible_moves_sorted = zip(*sorted(zip(possible_moves, scores_possible_moves)))

    return [move for move in possible_moves_sorted]


def is_terminal_state(board, current_piece):
    from Board_Representation import get_moves
    if len(get_moves(board, current_piece)) == 0:
        return True
    else:
        return False


def is_board_quiet(board, current_piece, prev_move_row, prev_move_column):
    from Board_Representation import get_moves, isOnBoard
    if len(get_moves(board, current_piece)) == 1:
        return False

    if isOnBoard(prev_move_row, prev_move_column) == True:
        if (prev_move_row, prev_move_column) in CORNERS_LIST == True or (
                prev_move_row, prev_move_column) in ADJACENT_CORNERS_LIST == True:
            return False

    return True


def quiescence_search_alg(board, current_piece, current_depth, target_depth, prev_move_row, prev_move_column):
    if is_board_quiet(board, current_piece, prev_move_row, prev_move_column) == True or \
            current_depth == target_depth or is_terminal_state(board, current_piece) == True:
        return (None, None, heuristic_evaluation_function(board, computer_piece))

    if current_depth % 2 == 0:
        current_value = -math.inf
        current_row = -1
        current_column = -1
    else:
        current_value = math.inf
        current_row = -1
        current_column = -1

    valid_moves = ordering_moves(board, current_piece, current_depth)

    if len(valid_moves) == 0:
        return (None, None, 0)
    else:
        for move in valid_moves:
            board_modified = np.copy(board)
            add_piece_to_board(board_modified, move[0], move[1], current_piece)
            new_row, new_column, new_value = normal_search(board_modified, 3 - current_piece, current_depth + 1,
                                                           target_depth, move[0], move[1])

            if current_depth % 2 == 0:
                if new_value > current_value:
                    current_value = new_value
                    current_row = move[0]
                    current_column = move[1]
            else:
                if new_value < current_value:
                    current_value = new_value
                    current_row = move[0]
                    current_column = move[1]

        return (current_row, current_column, current_value)


def normal_search(board, current_piece, current_depth, target_depth, prev_move_row, prev_move_column):
    if is_terminal_state(board, current_piece) == True:
        return (None, None, heuristic_evaluation_function(board, computer_piece))

    if current_depth == target_depth:
        if is_board_quiet(board, current_piece, prev_move_row, prev_move_column) == True:
            return (None, None, heuristic_evaluation_function(board, computer_piece))
        else:
            return quiescence_search_alg(board, current_piece, 0, 3, prev_move_row, prev_move_column)

    if current_depth % 2 == 0:
        current_value = -math.inf
        current_row = -1
        current_column = -1
    else:
        current_value = math.inf
        current_row = -1
        current_column = -1

    valid_moves = ordering_moves(board, current_piece, current_depth)

    if len(valid_moves) == 0:
        return (None, None, 0)
    else:
        for move in valid_moves:
            board_modified = np.copy(board)
            add_piece_to_board(board_modified, move[0], move[1], current_piece)
            new_row, new_column, new_value = normal_search(board_modified, 3 - current_piece, current_depth + 1,
                                                           target_depth, move[0], move[1])

            if current_depth % 2 == 0:
                if new_value > current_value:
                    current_value = new_value
                    current_row = move[0]
                    current_column = move[1]
            else:
                if new_value < current_value:
                    current_value = new_value
                    current_row = move[0]
                    current_column = move[1]

        return (current_row, current_column, current_value)


def quiescence_search(board, piece, depth):
    best_row, best_column, best_score = normal_search(board, current_piece=piece, current_depth=0, target_depth=depth,
                                                      prev_move_row=-1, prev_move_column=-1)

    return (best_row, best_column)
