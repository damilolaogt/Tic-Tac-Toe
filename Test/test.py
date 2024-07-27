# tests/test_tic_tac_toe.py

import pytest
from your_tic_tac_toe_module import check_winner, is_full, minimax, find_best_move

def test_check_winner():
    board_x_win = [["X", "X", "X"], ["-", "-", "-"], ["-", "-", "-"]]
    board_o_win = [["O", "O", "O"], ["-", "-", "-"], ["-", "-", "-"]]
    board_no_win = [["X", "O", "X"], ["O", "X", "O"], ["O", "X", "X"]]

    assert check_winner(board_x_win, "X") == True
    assert check_winner(board_o_win, "O") == True
    assert check_winner(board_no_win, "X") == False
    assert check_winner(board_no_win, "O") == False

def test_is_full():
    full_board = [["X", "O", "X"], ["O", "X", "O"], ["O", "X", "X"]]
    empty_board = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]

    assert is_full(full_board) == True
    assert is_full(empty_board) == False

def test_minimax():
    board = [["X", "O", "X"], ["-", "O", "-"], ["-", "-", "-"]]
    assert minimax(board, 0, True) == 1  # O's turn

def test_find_best_move():
    board = [["X", "O", "X"], ["-", "O", "-"], ["-", "-", "-"]]
    assert find_best_move(board) == (2, 0)  # AI's best move
