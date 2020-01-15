import numpy as np
import math

from Heuristic_Evaluation import heuristic_evaluation_function

computer_piece = 2


def ordering_moves(board, current_piece, depth):
    from Board_Representation import get_moves

    possible_moves = get_moves(board, current_piece)
    scores_possible_moves = []

    for move in possible_moves:
        board_modified = np.copy(board)
        board_modified[move[0]][move[1]] = current_piece
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


def alpha_beta_pruning_alg(board, current_piece, alpha, beta, current_depth, target_depth):
    if current_depth == target_depth or is_terminal_state(board, current_piece) == True:
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
            board_modified[move[0]][move[1]] = current_piece
            new_row, new_column, new_value = alpha_beta_pruning_alg(board_modified, 3 - current_piece, alpha, beta,
                                                                    current_depth + 1, target_depth)

            if current_depth % 2 == 0:
                if new_value > current_value:
                    current_value = new_value
                    current_row = move[0]
                    current_column = move[1]
                alpha = max(alpha, new_value)
                if alpha >= beta:
                    break
            else:
                if new_value < current_value:
                    current_value = new_value
                    current_row = move[0]
                    current_column = move[1]
                beta = min(beta, new_value)
                if alpha >= beta:
                    break
        return (current_row, current_column, current_value)


def alpha_beta_pruning(board, piece, depth):
    best_row, best_column, best_score = alpha_beta_pruning_alg(board, current_piece=piece, alpha=-math.inf,
                                                               beta=math.inf,
                                                               current_depth=0, target_depth=depth)

    return (best_row, best_column)
