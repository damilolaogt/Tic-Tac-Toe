import math
import random

# ──────────────────────────────────────────────
#  Board helpers
# ──────────────────────────────────────────────

def make_board():
    """Return a fresh 3x3 board filled with dashes."""
    return [["-"] * 3 for _ in range(3)]


def print_board(board):
    """Print the board with grid lines. Empty cells show their 1-9 position number."""
    print()
    for r, row in enumerate(board):
        cells = []
        for c, cell in enumerate(row):
            if cell == "X":
                display = " X "
            elif cell == "O":
                display = " O "
            else:
                display = f" {r * 3 + c + 1} "   # show position hint
            cells.append(display)
        print("|".join(cells))
        if r < 2:
            print("---+---+---")
    print()


def check_winner(board, player):
    """Return True if *player* has three in a row, column, or diagonal."""
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True
        if all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False


def is_full(board):
    """Return True when no empty cell remains."""
    return not any(cell == "-" for row in board for cell in row)


# Move-ordering priority: centre (best pruning), corners, then edges.
# Trying stronger squares first causes alpha-beta to cut more branches,
# so the AI finds its winning line faster.
_MOVE_ORDER = [(1,1), (0,0),(0,2),(2,0),(2,2), (0,1),(1,0),(1,2),(2,1)]

def get_empty_cells(board):
    """Return empty cells sorted by move-ordering priority (centre → corners → edges)."""
    return [(r, c) for r, c in _MOVE_ORDER if board[r][c] == "-"]


# ──────────────────────────────────────────────
#  Minimax with alpha-beta pruning
# ──────────────────────────────────────────────

def minimax(board, depth, is_maximizing, alpha, beta):
    """
    Minimax algorithm with alpha-beta pruning.

    The AI plays as 'O' (maximising player).
    The human plays as 'X' (minimising player).

    Alpha-beta pruning skips branches that cannot possibly
    influence the final decision, cutting the average search-tree
    size dramatically without changing the result.

    Score convention:
      +10 - depth  ->  AI wins (prefer shallower / faster wins)
      -10 + depth  ->  Human wins (prefer shallower losses)
       0           ->  Draw
    """
    # Terminal checks
    if check_winner(board, "O"):
        return 10 - depth
    if check_winner(board, "X"):
        return depth - 10
    if is_full(board):
        return 0

    if is_maximizing:           # AI's turn ("O")
        max_eval = -math.inf
        for r, c in get_empty_cells(board):
            board[r][c] = "O"
            score = minimax(board, depth + 1, False, alpha, beta)
            board[r][c] = "-"
            max_eval = max(max_eval, score)
            alpha = max(alpha, score)
            if beta <= alpha:   # Beta cut-off: prune remaining siblings
                break
        return max_eval

    else:                       # Human's turn ("X")
        min_eval = math.inf
        for r, c in get_empty_cells(board):
            board[r][c] = "X"
            score = minimax(board, depth + 1, True, alpha, beta)
            board[r][c] = "-"
            min_eval = min(min_eval, score)
            beta = min(beta, score)
            if beta <= alpha:   # Alpha cut-off: prune remaining siblings
                break
        return min_eval


def find_best_move(board):
    """
    Evaluate every legal move with minimax + alpha-beta pruning and
    return the (row, col) of the AI's optimal choice.

    Moves are tried in priority order (centre → corners → edges) so that
    alpha-beta encounters good moves early and prunes more branches,
    making the AI respond faster — especially on the first move.

    When multiple moves share the best score (i.e. they are all equally
    optimal), one is chosen at random. This keeps the AI unbeatable while
    preventing the repetitive, predictable pattern that a deterministic
    first-found search produces.
    """
    best_score = -math.inf
    best_moves = []

    for r, c in get_empty_cells(board):
        board[r][c] = "O"
        score = minimax(board, 0, False, -math.inf, math.inf)
        board[r][c] = "-"
        if score > best_score:
            best_score = score
            best_moves = [(r, c)]   # new best — reset candidate list
        elif score == best_score:
            best_moves.append((r, c))  # tied — add to candidates

    # Random pick among equally good moves
    return random.choice(best_moves)


# ──────────────────────────────────────────────
#  Input helpers
# ──────────────────────────────────────────────

def get_player_move(board):
    """
    Prompt the human for a valid move (1-9) and return (row, col).
    Loops until the input is a valid, unoccupied cell.
    """
    while True:
        try:
            move = int(input("Your move (1-9): "))
            if not (1 <= move <= 9):
                print("  Please enter a number between 1 and 9.")
                continue
            r, c = (move - 1) // 3, (move - 1) % 3
            if board[r][c] != "-":
                print("  That cell is already taken. Choose another.")
                continue
            return r, c
        except ValueError:
            print("  Invalid input - please type a whole number (1-9).")


# ──────────────────────────────────────────────
#  Main game loop
# ──────────────────────────────────────────────

def play_game():
    board = make_board()

    print("\n" + "=" * 37)
    print("   TIC-TAC-TOE  -  You (X) vs AI (O)")
    print("=" * 37)
    print_board(board)

    while True:
        # Human's turn
        print("Your turn (X):")
        r, c = get_player_move(board)
        board[r][c] = "X"
        print_board(board)

        if check_winner(board, "X"):
            print("You win! Congratulations!")
            return

        if is_full(board):
            print("It's a draw!")
            return

        # AI's turn
        print("AI is thinking...")
        ai_r, ai_c = find_best_move(board)
        board[ai_r][ai_c] = "O"
        print(f"AI played position {ai_r * 3 + ai_c + 1}.")
        print_board(board)

        if check_winner(board, "O"):
            print("AI wins! Better luck next time.")
            return

        if is_full(board):
            print("It's a draw!")
            return


def main():
    while True:
        play_game()
        answer = input("Play again? (y/n): ").strip().lower()
        if answer not in ("y", "yes"):
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()


