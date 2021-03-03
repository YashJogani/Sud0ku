from time import time

board = [
    [1, 0, 0, 4, 8, 9, 0, 0, 6],
    [7, 3, 0, 0, 5, 0, 0, 4, 0],
    [4, 6, 0, 0, 0, 1, 2, 9, 5],
    [3, 8, 7, 1, 2, 0, 6, 0, 0],
    [5, 0, 1, 7, 0, 3, 0, 0, 8],
    [0, 4, 6, 0, 9, 5, 7, 1, 0],
    [9, 1, 4, 6, 0, 0, 0, 8, 2],
    [0, 2, 0, 0, 4, 0, 0, 3, 7],
    [8, 0, 3, 5, 1, 2, 0, 0, 4]
]

board2 = [
    [4, 0, 6, 3, 8, 0, 0, 2, 0],
    [5, 0, 3, 7, 0, 4, 0, 0, 0],
    [0, 0, 0, 9, 0, 0, 8, 4, 3],
    [2, 3, 0, 0, 1, 0, 9, 0, 0],
    [0, 4, 0, 0, 0, 0, 5, 7, 1],
    [0, 5, 0, 6, 4, 7, 0, 0, 0],
    [9, 0, 1, 4, 0, 8, 3, 0, 0],
    [0, 6, 4, 0, 0, 0, 0, 0, 7],
    [8, 0, 5, 1, 0, 3, 0, 9, 2]
]


# backtrack algorithm to solve sudoku board

def solve(board):
    # this will store empty spots so we can use it later when we backtrack
    # (x, y): n
    empty = {}

    # finds empty spots in board
    find = find_empty(board)
    n = 1

    while find:
        row, col = find
        for i in range(n, 10):
            if valid(board, i, (row, col)):
                # writes the number in empty spot
                # and stores that location
                board[row][col] = i
                empty[(row, col)] = i
                fill = True
                break
            else:
                fill = False

        if not fill:
            # if no number is valid
            # then we backtrack to last spot using empty dict
            find = list(empty)[-1]
            n = empty[find] + 1
            board[find[0]][find[1]] = 0
            empty.popitem()

        else:
            n = 1
            find = find_empty(board)


def solve_recursive(board):
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(board, i, (row, col)):
            board[row][col] = i
            if solve_recursive(board):
                return True

            board[row][col] = 0

    return False


def valid(board, num, pos):
    # check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # check column
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # check box
    box_x = pos[1]//3
    box_y = pos[0]//3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if board[i][j] == num and pos != (i, j):
                return False

    return True


def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0:
            print("-------------------------")

        for j in range(len(board[0])):
            if j % 3 == 0:
                print("| ", end="")

            print(board[i][j], end=" ")

            if j % 8 == 0 and j != 0:
                print("| ", end="")

        print("")
        if i % 8 == 0 and i != 0:
            print("-------------------------")


def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return i, j
    return False


def correct(board):
    for i in range(9):
        for j in range(9):
            solution = valid(board, board[i][j], (i, j))
            if not solution:
                break
        if not solution:
            break
    print(solution)


start = time()
solve(board)
print((time() - start)*1000)
print_board(board)
correct(board)
