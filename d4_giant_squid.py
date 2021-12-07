from AoCGui import AoCGui

EXAMPLE_DATA = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""


class SquidGame(AoCGui):
    def __init__(self):
        super().__init__()
        self.winning_numbers = []
        self.bingo_boards = []
        self.win = False
        self.to_remove_board = []
        self.last_winning_board = None
        self.prepare_gui("Day 4: Giant Squid", "Calculate Winning Board", EXAMPLE_DATA)

    def button_pressed(self):
        self.load_text_box_data()
        self.data_lines.pop()
        winning_numbers_string = self.data_lines.pop(0)
        self.winning_numbers = [x.strip() for x in winning_numbers_string.split(",") if x != ""]
        while len(self.data_lines) > 5:
            self.data_lines.pop(0)
            self.bingo_boards.append(BingoBoard(self.data_lines[:5]))
            self.data_lines = self.data_lines[5:]
        if self.part.get() == 1:
            self.part_one()
        else:
            self.part_two()

    def part_one(self):
        while not self.win and len(self.winning_numbers) > 0:
            self.process_next_number_one()
        if not self.win:
            print("No winning board found")
            self.print_boards()

    def part_two(self):
        while self.bingo_boards and len(self.winning_numbers) > 0:
            self.process_next_number_two()
            while self.to_remove_board:
                self.bingo_boards.remove(self.to_remove_board.pop(0))
        self.write_result(f"Last winning board had score: {self.last_winning_board.score}")
        print(self.last_winning_board)

    def process_next_number_one(self):
        number = self.winning_numbers.pop(0)
        print(f"Marking number {number}")
        for board in self.bingo_boards:
            board.check_number(number)
            if board.win:
                self.win = True
                self.write_result(f"Winning board found with score: {board.score}")
                return

    def process_next_number_two(self):
        number = self.winning_numbers.pop(0)
        print(f"Marking number {number}")
        for board in self.bingo_boards:
            board.check_number(number)
            if board.win:
                self.win = True
                self.last_winning_board = board
                self.to_remove_board.append(board)

    def print_boards(self):
        for board in self.bingo_boards:
            print(board)


class BingoBoard:
    def __init__(self, row_list):
        self.board = [["0"] * 5, ["0"] * 5, ["0"] * 5, ["0"] * 5, ["0"] * 5]
        self.create_board(row_list)
        # print(self.board)
        self.score = 0
        self.win = False
        self.last_mark = []

    def create_board(self, row_string):
        for row in range(5):
            # Filter out additional blanks
            row_list = [x.strip(" ") for x in row_string[row].split(" ") if x != ""]
            self.board[row] = row_list

    # Marks number and checks for win
    def check_number(self, number):
        marked = self.mark_number(number)
        if marked:
            self.check_winning_row(self.last_mark[0])
            self.check_winning_column(self.last_mark[1])
        if self.win:
            self.score_board(number)

    def mark_number(self, number) -> bool:
        for row in range(5):
            for column in range(5):
                if self.board[row][column] == number:
                    self.board[row][column] = "x"
                    self.last_mark = [row, column]
                    return True
        return False

    def row_as_string(self, row_number):
        return " ".join([x if len(x) > 1 else " " + x for x in self.board[row_number]])

    def check_winning_row(self, row_number):
        if (self.board[row_number][0] == "x" and
            self.board[row_number][1] == "x" and
            self.board[row_number][2] == "x" and
            self.board[row_number][3] == "x" and
            self.board[row_number][4] == "x"
           ):
            self.win = True

    def check_winning_column(self, column_number):
        if (self.board[0][column_number] == "x" and
            self.board[1][column_number] == "x" and
            self.board[2][column_number] == "x" and
            self.board[3][column_number] == "x" and
            self.board[4][column_number] == "x"
        ):
            self.win = True

    def __repr__(self):
        board_string = (f"{self.row_as_string(0)}\n"
                        f"{self.row_as_string(1)}\n"
                        f"{self.row_as_string(2)}\n"
                        f"{self.row_as_string(3)}\n"
                        f"{self.row_as_string(4)}\n")
        return board_string

    def score_board(self, winning_number):
        score = 0
        for row in range(5):
            for column in range(5):
                if self.board[row][column] != "x":
                    score += int(self.board[row][column])
        score *= int(winning_number)
        self.score = score


if __name__ == "__main__":
    squid_game = SquidGame()
