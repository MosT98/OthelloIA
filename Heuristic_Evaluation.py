ROWS = 8
COLUMNS = 8
DIRECTIONS = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]  # NV, N, NE, E, V, SV, S, SE


# Coin Parity
def coin_parity(board, current_piece, other_piece):
    counter_current_piece = 0
    counter_other_piece = 0
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == current_piece:
                counter_current_piece += 1
            elif board[row][col] == other_piece:
                counter_other_piece += 1

    coin_parity_heuristic_value = 100 * (counter_current_piece - counter_other_piece) / (
            counter_current_piece + counter_other_piece)
    return coin_parity_heuristic_value


# Actual Mobility
def actual_mobility(board, current_piece, other_piece):
    from Board_Representation import get_moves
    counter_legal_moves_current_piece = len(get_moves(board, current_piece))
    counter_legal_moves_other_piece = len(get_moves(board, other_piece))

    actual_mobility_heuristic_value = 0
    if counter_legal_moves_current_piece + counter_legal_moves_other_piece != 0:
        actual_mobility_heuristic_value = 100 * (
                counter_legal_moves_current_piece - counter_legal_moves_other_piece) / (
                                                  counter_legal_moves_current_piece + counter_legal_moves_other_piece)
    return actual_mobility_heuristic_value


# Potential Mobility
def count_empty_moves(board, row, col):
    from Board_Representation import isOnBoard, isValidLocation
    counter = 0
    for x, y in DIRECTIONS:
        new_row = row + x
        new_col = col + y
        if isOnBoard(new_row, new_col) and isValidLocation(board, row, col):
            counter += 1
    return counter


def get_potential_moves(board, piece):
    potential_moves = 0
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == piece:
                potential_moves += count_empty_moves(board, row, col)
    return potential_moves


def potential_mobility(board, current_piece, other_piece):
    counter_potential_moves_current_piece = get_potential_moves(board, other_piece)
    counter_potential_moves_other_piece = get_potential_moves(board, current_piece)

    potential_mobility_heuristic_value = 0
    if counter_potential_moves_current_piece + counter_potential_moves_other_piece != 0:
        potential_mobility_heuristic_value = 100 * (
                counter_potential_moves_current_piece - counter_potential_moves_other_piece) / (
                                                     counter_potential_moves_current_piece + counter_potential_moves_other_piece)
    return potential_mobility_heuristic_value


# Corners Captured
def corners_captured(board, current_piece, other_piece):
    corners_current_piece = 0
    corners_other_piece = 0

    if board[0][0] == current_piece:
        corners_current_piece += 1
    elif board[0][0] == other_piece:
        corners_other_piece += 1
    if board[0][7] == current_piece:
        corners_current_piece += 1
    elif board[0][7] == other_piece:
        corners_other_piece += 1
    if board[7][0] == current_piece:
        corners_current_piece += 1
    elif board[7][0] == other_piece:
        corners_other_piece += 1
    if board[7][7] == current_piece:
        corners_current_piece += 1
    elif board[7][7] == other_piece:
        corners_other_piece += 1

    corner_heuristic_value = 0
    if corners_current_piece + corners_other_piece != 0:
        corner_heuristic_value = 100 * (corners_current_piece - corners_other_piece) / (
                corners_current_piece + corners_other_piece)
    return corner_heuristic_value


# Stability
def get_piece_stability(board, piece):
    score = 0

    if board[1][0] == piece:
        if board[0][0] == piece:
            score += 1
        else:
            score -= 1
    if board[1][1] == piece:
        if board[0][0] == piece:
            score += 1
        else:
            score -= 1
    if board[0][1] == piece:
        if board[0][0] == piece:
            score += 1
        else:
            score -= 1

    if board[0][6] == piece:
        if board[0][7] == piece:
            score += 1
        else:
            score -= 1
    if board[1][6] == piece:
        if board[0][7] == piece:
            score += 1
        else:
            score -= 1
    if board[1][7] == piece:
        if board[0][7] == piece:
            score += 1
        else:
            score -= 1

    if board[6][0] == piece:
        if board[7][0] == piece:
            score += 1
        else:
            score -= 1
    if board[6][1] == piece:
        if board[7][0] == piece:
            score += 1
        else:
            score -= 1
    if board[7][1] == piece:
        if board[7][0] == piece:
            score += 1
        else:
            score -= 1

    if board[7][6] == piece:
        if board[7][7] == piece:
            score += 1
        else:
            score -= 1
    if board[6][6] == piece:
        if board[7][7] == piece:
            score += 1
        else:
            score -= 1
    if board[6][7] == piece:
        if board[7][7] == piece:
            score += 1
        else:
            score -= 1

    for col in range(2, 6):
        if board[0][col] == piece:
            score += 1
        if board[7][col] == piece:
            score += 1
    for lin in range(2, 6):
        if board[lin][0] == piece:
            score += 1
        if board[lin][7] == piece:
            score += 1

    return score


def stability(board, current_piece, other_piece):
    stability_current_piece = get_piece_stability(board, current_piece)
    stability_other_piece = get_piece_stability(board, other_piece)

    stability_heuristic_value = 0
    if stability_current_piece + stability_other_piece != 0:
        stability_heuristic_value = 100 * (stability_current_piece - stability_other_piece) / (
                stability_current_piece + stability_other_piece)
    return stability_heuristic_value


def heuristic_evaluation_function(board, current_piece):
    other_piece = 3 - current_piece

    return coin_parity(board, current_piece, other_piece) + actual_mobility(board, current_piece, other_piece) + \
           potential_mobility(board, current_piece, other_piece) + corners_captured(board, current_piece, other_piece) + \
           stability(board, current_piece, other_piece)
