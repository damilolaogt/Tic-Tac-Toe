def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True 
        if all(board[j][i] == player for j in range(3)):
            return True            
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
        return True
    return False

a = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]
design = "1 2 3\n4 5 6\n7 8 9"
print(design)
playToMove = str(1)

while "-" in [item for sublist in a for item in sublist]:
    i = input("Player " + playToMove + ", what is your move between 1 and 9: ")

    move = int(i)
    if 1 <= move <= 9 and a[(move - 1) // 3][(move - 1) % 3] == "-":
        if playToMove == "1":
            value = "x"
        else:
            value = "o"
        a[(move - 1) // 3][(move - 1) % 3] = value
        design = design.replace(i, value)
        print(design)

        if check_winner(a, value):
            print("Player " + playToMove + " wins!")
            break

        if "-" not in [item for sublist in a for item in sublist]:
            print("It's a draw!")
            break

        if playToMove == "1":
            playToMove = "2"
        else:
            playToMove = "1"
    else:
        print("Invalid move. Try again.")
else:
    print("Invalid input. Please enter a number between 1 and 9.")

