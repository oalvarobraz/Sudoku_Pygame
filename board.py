class BoardSudoku:

    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.vetor = []

    def can_insert(self, x: int, y: int, player: int) -> bool:
        if self.get_status(x, y) != 0:
            return False

        # Check row
        if player in self.board[x]:
            return False

        # Check column
        if player in [self.board[i][y] for i in range(9)]:
            return False

        # Check sub-matrix 3x3
        sub_matrix_x = (x // 3) * 3
        sub_matrix_y = (y // 3) * 3
        for i in range(sub_matrix_x, sub_matrix_x + 3):
            for j in range(sub_matrix_y, sub_matrix_y + 3):
                if self.board[i][j] == player:
                    return False

        return True

    def is_full(self):
        return all(self.board[i][j] != 0 for i in range(9) for j in range(9))

    def display(self):
        for i in range(9):
            for j in range(9):
                if j == 3 or j == 6:
                    print("\t\t\t\t", end='')
                print(f"\t| {self.board[i][j]} |", end='')
            if i == 2 or i == 5:
                print('\n\n')
            else:
                print("\t\t\n")

    def get_status(self, x: int, y: int):
        return self.board[x][y]

    def insert(self, x: int, y: int, player: int):
        if 1 <= player <= 9 and 0 <= x <= 8 and 0 <= y <= 8:
            if not self.vetor.__contains__((x, y)):
                self.board[x][y] = player
                return 1
        else:
            return -1

    def erase(self, x: int, y: int):
        if not self.vetor.__contains__((x, y)):
            self.board[x][y] = 0

    def check(self):
        if not self.is_full():
            return False

        # Check rows
        for i in range(9):
            if len(set(self.board[i])) != 9:
                return False

        # Check columns
        for j in range(9):
            if len(set([self.board[i][j] for i in range(9)])) != 9:
                return False

        # Check 3x3 sub-grids
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                if len(set([self.board[x][y] for x in range(i, i + 3) for y in range(j, j + 3)])) != 9:
                    return False

        return True

    def upload_arq(self, file_name):
        with open(file_name, "r") as file:
            for line in file:
                x, y, player = map(int, line.strip().split())
                self.insert(x, y, player)
                self.vetor.append((x, y))

    def upload_answer(self, file_name):
        with open(file_name, "r") as file:
            for i, line in enumerate(file):
                for j, val in enumerate(line.split()):
                    self.board[i][j] = int(val)
                    self.vetor.append((i, j))


