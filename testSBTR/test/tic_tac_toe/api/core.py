"""
This algorithm was taken from the book
Invent_Your_Own_Computer_Games_with_Python_by_Al_Sweigart.
Code was a bit refactored, but just a bit.
"""

import random


def make_move(board, letter, move):
    board[move] = letter


def choose_side():
    if random.randint(0, 1) == 0:
        return "X"
    else:
        return "O"


def is_winner(board, letter):
    """
    Given a board and a player's letter, this function returns True if that player has won.
    We use bo instead of board and le instead of letter so we don't have to type as much.
    :param board: list
    :param letter: str
    :return: bool
    """
    return (
        # across the top
        (board[0] == letter and board[1] == letter and board[2] == letter)
        or
        # across the middle
        (board[3] == letter and board[4] == letter and board[5] == letter)
        or
        # across the bottom
        (board[6] == letter and board[7] == letter and board[8] == letter)
        or
        # down the left side
        (board[6] == letter and board[3] == letter and board[0] == letter)
        or
        # down the middle
        (board[7] == letter and board[4] == letter and board[1] == letter)
        or
        # down the right side
        (board[8] == letter and board[5] == letter and board[2] == letter)
        or
        # diagonal
        (board[0] == letter and board[4] == letter and board[8] == letter)
        or
        # diagonal
        (board[2] == letter and board[4] == letter and board[6] == letter)
    )


def get_board_copy(board):
    # Make a copy of the board list and return it.
    board_copy = []
    for i in board:
        board_copy.append(i)
    return board_copy


def is_space_free(board, move):
    # Return true if the passed move is free on the passed board.
    return board[move] != "X" and board[move] != "O"


def choose_random_move_from_list(board, moves_list):
    # Returns a valid move from the passed list on the passed board.
    # Returns None if there is no valid move.
    possible_moves = []
    for i in moves_list:
        if is_space_free(board, i):
            possible_moves.append(i)

    if len(possible_moves) != 0:
        return random.choice(possible_moves)
    # else:
    #     return None


def get_move(board, ai_letter):
    # Given a board and the computer's letter, determine where to move and return that move.
    if ai_letter == "X":
        player_letter = "O"
    else:
        player_letter = "X"

    # Here is our algorithm for our Tic Tac Toe AI:
    # First, check if we can win in the next move
    for i in range(9):
        board_copy = get_board_copy(board)
        if is_space_free(board_copy, i):
            make_move(board_copy, ai_letter, i)
            if is_winner(board_copy, ai_letter):
                return i

    # Check if the player could win on his next move, and block them.
    for i in range(9):
        board_copy = get_board_copy(board)
        if is_space_free(board_copy, i):
            make_move(board_copy, player_letter, i)
            if is_winner(board_copy, player_letter):
                return i

    # Try to take one of the corners, if they are free.
    move = choose_random_move_from_list(board, [0, 2, 6, 8])
    if move is None:
        return move

    # Try to take the center, if it is free.
    if is_space_free(board, 4):
        return 4
    # Move on one of the sides.
    return choose_random_move_from_list(board, [2, 4, 6, 8])


def is_board_full(board):
    # Return True if every space on the board has been taken. Otherwise return False.
    # for i in range(1, 10):
    return all(False for i in range(9) if is_space_free(board, i))
