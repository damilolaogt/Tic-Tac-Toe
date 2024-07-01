import math

def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True 
        if all(board[j][i] == player for j in range(3)):
            return True            
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    return not any("-" in row for row in board)

def minimax(board, depth, is_maximizing):
    if check_winner(board, "X"):
        return -10 + depth
    if check_winner(board, "O"):
        return 10 - depth
    if is_full(board):
        return 0

    if is_maximizing:
        max_eval = -math.inf    
        for i in range(3):
            for j in range(3):
                if board[i][j] == "-":
                    board[i][j] = "O"
                    eval = minimax(board, depth + 1, False)
                    board[i][j] = "-"
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == "-":
                    board[i][j] = "X"
                    eval = minimax(board, depth + 1, True)
                    board[i][j] = "-"
                    min_eval = min(min_eval, eval)
        return min_eval

def find_best_move(board):
    best_move = None
    best_eval = -math.inf
    for i in range(3):
        for j in range(3):
            if board[i][j] == "-":
                board[i][j] = "O"
                eval = minimax(board, 0, False)
                board[i][j] = "-"
                if eval > best_eval:
                    best_eval = eval
                    best_move = (i, j)
    return best_move

a = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]
design = "1 2 3\n4 5 6\n7 8 9"
print(design)
playToMove = str(1)

while "-" in [item for sublist in a for item in sublist]:
    i = input("Player " + playToMove + ", what is your move between 1 and 9: ")

    move = int(i)
    if 1 <= move <= 9 and a[(move - 1) // 3][(move - 1) % 3] == "-":
        if playToMove == "1":
            value = "X"
        else:
            value = "O"
        a[(move - 1) // 3][(move - 1) % 3] = value
        design = design.replace(i, value)
        print(design)

        if check_winner(a, value):
            print("Player " + playToMove + " wins!")
            break

        if is_full(a):
            print("It's a draw!")
            break

        if playToMove == "1":
            playToMove = "2"
        else:
            playToMove = "1"
            
        if playToMove == "2" and "-" in [item for sublist in a for item in sublist]:
            print("AI's turn...")
            ai_move = find_best_move(a)
            a[ai_move[0]][ai_move[1]] = "O"
            design = design.replace(str(ai_move[0] * 3 + ai_move[1] + 1), "O")
            print(design)

            if check_winner(a, "O"):
                print("AI wins!")
                break

            if is_full(a):
                print("It's a draw!")
                break

            playToMove = "1"
    else:
        print("Invalid move. Try again.")
else:
    print("Invalid input. Please enter a number between 1 and 9.")

