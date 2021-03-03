from copy import deepcopy
## backtrack algorithm to solve sudoku board

class Solve:
    def __init__(self, board, copy):
        if copy:
            self.board = deepcopy(board)
        else:
            self.board = board

        ## this will store empty spots so we can use it later when we backtrack
        ## (x, y): n
        self.empty = {}
        ## finds empty spots in board
        self.find = self.find_empty()
        self.n = 1

    def valid(self, num, pos):
        ## check row
        for i in range(len(self.board[0])):
            if self.board[pos[0]][i] == num and pos[1] != i:
                return False

        ## check column
        for i in range(len(self.board)):
            if self.board[i][pos[1]] == num and pos[0] != i:
                return False

        # check box
        box_x = pos[1]//3
        box_y = pos[0]//3

        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x*3, box_x*3 + 3):
                if self.board[i][j] == num and pos != (i, j):
                    return False

        return True

    def find_empty(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    return i, j
        return False

    def __next__(self):
        while self.find:
            self.row, self.col = self.find
            for i in range(self.n, 10):
                if self.valid(i, (self.row, self.col)):
                    ## writes the number in empty spot
                    ## and stores that location
                    self.board[self.row][self.col] = i
                    self.empty[(self.row, self.col)] = i
                    self.fill = True
                    break
                else:
                    self.fill = False

            if not self.fill:
                ## if no number is valid
                ## then we backtrack to last spot using empty dict
                self.find = list(self.empty)[-1]
                self.n = self.empty[self.find] + 1
                self.board[self.find[0]][self.find[1]] = 0
                self.empty.popitem()

            else:
                self.n = 1
                self.find = self.find_empty()

            return self.row, self.col
