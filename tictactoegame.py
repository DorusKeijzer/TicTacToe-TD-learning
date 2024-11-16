
from os import makedev


class Game:
    def __init__(self, num = 0):
        self.board = self._decimal_to_tic_tac_toe(num)

    def place(self, checkvalue: str, row: int, col: int):
        if self.board[row][col] != " ":
            raise Exception(f"{row}, {col} already occupied")
        self.board[row][col] = checkvalue

    def unplace(self, row: int, col: int):
        if self.board[row][col] == " ":
            raise Exception(f"{row}, {col} not occupied")
        self.board[row][col] = ""

    def _count(self, checkvalue: str):
        res = 0
        for col in range(3):
            for row in range(3):
                if self.board[col][row] == checkvalue:
                    res+=1

        return res     
    
    def wins(self, checkvalue: str):
        return self._count_rows(checkvalue) + self._count_cols(checkvalue) + self._count_diagonals(checkvalue) > 0


    def _get_state_num(self):
        """Gets the state number belonging to the current state"""
        res = 0
        index = 0
        for i in reversed(range(3)):
            for j in reversed(range(3)):
                if self.board[i][j] == "x":
                    res += 3 ** index 
                if self.board[i][j] == "o":
                    res += 2 * 3 ** index
                index += 1
        return res

    def free_states(self, checkvalue: str) -> list[int]:
        res = []
        free_squares = self._free_squares()
        for row,col in free_squares:
            self.place(checkvalue, row, col)
            res.append(self._get_state_num())
            self.unplace(row, col)
        return res

    def _free_squares(self):
        free = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    free.append((i,j))
        return free

    def _islegal(self):
        xs, os = self._count("x"), self._count("o")

        # Check turn order
        numbers_ok = xs == os or xs == os + 1
        if not numbers_ok:
            return False

        x_wins = self._count_rows("x") + self._count_cols("x") + self._count_diagonals("x")
        o_wins = self._count_rows("o") + self._count_cols("o") + self._count_diagonals("o")

        # Check for multiple winners or invalid turn order
        if (x_wins > 0 and o_wins > 0) or (x_wins > 0 and xs != os + 1) or (o_wins > 0 and xs != os):
            return False

        return True


    def draw(self):
        for i in range(3):
            print("-------------")
            print(f"| {self.board[i][0]} | {self.board[i][1]} | {self.board[i][2]} |")
        print("-------------")

    def _check_rows(self, checkvalue):
        for i in range(3):
            res = True
            for j in range(3):
                if self.board[i][j] != checkvalue:
                    res = False
            if res:
                return True

        return False

    def _count_rows(self, checkvalue: str):
        numrows = 0
        
        for i in range(3):
            res = True
            for j in range(3):
                if self.board[i][j] != checkvalue:
                    res = False
            if res:
                numrows+=1

        return numrows

    def _count_cols(self, checkvalue: str):
        num_cols = 0
        
        for i in range(3):
            res = True
            for j in range(3):
                if self.board[j][i] != checkvalue:
                    res = False
            if res:
                num_cols += 1

        return num_cols

    def _check_cols(self, checkvalue: str):
        for i in range(3):
            res = True
            for j in range(3):
                if self.board[j][i] != checkvalue:
                    res = False
            if res:
                return True

        return False
    
    def _check_diagonals(self, checkvalue: str):
        res = True
        for i in range(3):
            if self.board[i][i] != checkvalue:
                res = False
        if res: 
            return True
        res = True
        for i in range(3):
            if self.board[2-i][i] != checkvalue:
                res = False
        if res:
            return True

    def _count_diagonals(self, checkvalue: str):
        num_diags = 0

        res = True
        for i in range(3):
            if self.board[i][i] != checkvalue:
                res = False
        if res: 
            num_diags += 1
        res = True
        for i in range(3):
            if self.board[2-i][i] != checkvalue:
                res = False
        if res:
            num_diags += 1 

        return num_diags

    def update_state(self, state: int):
        self.board = self._decimal_to_tic_tac_toe(state)

    def _decimal_to_tic_tac_toe(self, index):
        if index < 0 or index >= 3**9:
            raise ValueError("Index out of range. Must be between 0 and 19682.")
        
        # Convert index to a base-3 (ternary) representation
        ternary = ""
        for _ in range(9):
            ternary = str(index % 3) + ternary
            index //= 3
        
        # Map ternary digits to Tic-Tac-Toe symbols
        board = []
        symbol_map = {'0': ' ', '1': 'x', '2': 'o'}
        for i in range(0, 9, 3):
            row = [symbol_map[ternary[j]] for j in range(i, i + 3)]
            board.append(row)
        return board

if __name__ == "__main__":
    b = Game(33)
    print("current:")
    b.draw()
    for free in b.free_states("x"):
        print(free)
        g = Game(free)
        g.draw()
