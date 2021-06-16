"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    iksy = 0
    kolka = 0

    for row in board:
        for tile in row:
            if tile == X:
                iksy += 1

            elif tile == O:
                kolka += 1

    if iksy > kolka:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()

    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                moves.add((row, col))

    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid action")

    else:
        new_board = copy.deepcopy(board)
        new_board[action[0]][action[1]] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # rows
    for i in range(3):
        if all(a == board[i][0] for a in board[i]):
            return board[i][0]

    # columns
    for i in range(3):
        if board[0][i] == board[1][i] and board[1][i] == board[2][i]:
            return board[0][i]

    # diagonals
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    elif board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[0][2]
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    elif not any(EMPTY in row for row in board):
        return True

    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        elif winner(board) is None:
            return 0

    else:
        raise NameError('Board not terminal')


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    Max = -math.inf
    Min = math.inf

    if player(board) == X:
        return maxx(board, Max, Min)[1]

    else:
        return minn(board, Max, Min)[1]


def maxx(board, alpha, beta):
    if terminal(board):
        return utility(board), None

    move = None
    value = -math.inf

    for action in actions(board):
        contr_value, contr_move = minn(result(board, action), alpha, beta)
        alpha = max(alpha, contr_value)

        if contr_value > value:
            value = contr_value
            move = action

        if alpha >= beta:
            break

    return value, move


def minn(board, alpha, beta):
    if terminal(board):
        return utility(board), None

    move = None
    value = math.inf

    for action in actions(board):
        contr_value, contr_move = maxx(result(board, action), alpha, beta)
        beta = min(beta, contr_value)

        if contr_value < value:
            value = contr_value
            move = action

        if alpha >= beta:
            break

    return value, move
