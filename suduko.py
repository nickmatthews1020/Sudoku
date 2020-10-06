class SudokuPuzzle:
    
    class Square:
        def __init__(self, value, attempts, fixed):
            self.value = value
            self.attempts = attempts
            self.fixed = fixed

        def setValue(self, value):
            self.value = value

        def addAttempt(self, attempt):
            self.attempts.append(attempt)

        def clearAttempts(self):
            self.attempts = []

        def isFixed(self):
            return self.fixed

    def __init__(self, puzzle):
        self.solved = False
        self.puzzle = []
        for i in range (0, 9):
            row = []
            for j in range (0, 9):
                value = puzzle[i][j]
                row.append(SudokuPuzzle.Square(value, [], value != 0))
            self.puzzle.append(row)

    def print_puzzle(self):
        for i in range (0, 9):
            row = []
            for j in range (0, 9):
                row.append(self.puzzle[i][j].value)
            print (row)
        print()

    def intersect_calculator(self, row, column):
        rows = []
        columns = []
        square = []

        for i in range(0, 9):
            if (i != row):
                rows.append(self.puzzle[i][column].value)
            if (i != column):
                columns.append(self.puzzle[row][i].value)
        for i in range (0, 3):
            for j in range (0, 3):
                x = i + 3*(row//3)
                y = j + 3*(column//3)
                if (not(x == row and y == column)):
                    square.append(self.puzzle[x][y].value)

        return [rows, columns, square]

    def valid(self, row, column, value):
        intersects = self.intersect_calculator(row, column)
        if (value in self.puzzle[row][column].attempts):
            return False
        for i in range(0, 3):
            if (value in intersects[i]):
                return False
        return True

    def find_value(self, row, column):
        for i in range (1, 10):
            if self.valid(row, column, i):
                self.puzzle[row][column].setValue(i)
                self.puzzle[row][column].addAttempt(i)
                return i
        self.puzzle[row][column].setValue(0)
        return 0

    def solve_square(self, row, column):
        self.puzzle[row][column].clearAttempts()

        next_row = row
        next_column = column
        if (column == 8):
            next_column = 0
            next_row += 1
        else:
            next_column += 1

        if (row == 8 and column == 8):
            self.find_value(row, column)
            self.solved = True
        elif (self.puzzle[row][column].isFixed()):
            self.solve_square(next_row, next_column)
        else:
            while (not(self.solved) and (self.find_value(row, column) != 0)):
                self.solve_square(next_row, next_column)

    def solve_puzzle(self):
        self.solve_square(0, 0)
