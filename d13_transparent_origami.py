from AoCGui import AoCGui

EXAMPLE_DATA = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""


class TransparentOrigami(AoCGui):
    def __init__(self):
        super().__init__()
        self.dots = []
        self.instructions = []
        self.paper = {}
        self.max_x = 0
        self.max_y = 0
        self.prepare_gui("Day 13: Transparent Origami", "Calculate Dots", EXAMPLE_DATA)

    def button_pressed(self):
        self.load_text_box_data()
        self.data_lines.pop()
        self.read_data()
        # print(self.data_lines)
        if self.part.get() == 1:
            self.part_one()
        else:
            self.part_two()

    def part_one(self):
        # print("Before fold:")
        # self.print_paper()
        instruction = self.instructions.pop(0)
        axis, fold_index = instruction.split("=")
        fold_index = int(fold_index)
        axis = axis[-1]
        if axis == "y":
            self.fold_on_y_axis(fold_index)
        elif axis == "x":
            self.fold_on_x_axis(fold_index)
        # print("After fold:")
        # self.print_paper()
        number_of_dots = 0
        for value in self.paper.values():
            number_of_dots += len(value)
        self.write_result(f"Number of Dots: {number_of_dots}")

    def part_two(self):
        while self.instructions:
            instruction = self.instructions.pop(0)
            axis, fold_index = instruction.split("=")
            fold_index = int(fold_index)
            axis = axis[-1]
            if axis == "y":
                self.fold_on_y_axis(fold_index)
            elif axis == "x":
                self.fold_on_x_axis(fold_index)
        result_string = self.print_paper()
        self.write_result(result_string)

    def read_data(self):
        instructions_index = self.data_lines.index("")
        self.dots = self.data_lines[:instructions_index]
        self.instructions = self.data_lines[instructions_index+1:]
        # print(f"Dots: {self.dots}")
        # print(f"Instructions: {self.instructions}")
        for dot_string in self.dots:
            x, y = [int(a) for a in dot_string.split(",")]
            self.max_x = max(x, self.max_x)
            self.max_y = max(y, self.max_y)
            if y in self.paper.keys():
                self.paper[y].append(x)
            else:
                self.paper[y] = [x]
        print(self.paper)
        print(f"Max: {self.max_x} {self.max_y}")

    def fold_on_y_axis(self, fold_index):
        # rows_before_index = [row_index for row_index in self.paper.keys() if row_index < fold_index]
        rows_after_index = [row_index for row_index in self.paper.keys() if row_index > fold_index]
        for row_number in rows_after_index:
            folded_row_number = fold_index - (row_number - fold_index)
            row = self.paper[row_number]
            if folded_row_number in self.paper.keys():
                fold_on_row = self.paper[folded_row_number]
                for element in row:
                    if element not in fold_on_row:
                        fold_on_row.append(element)
                self.paper[folded_row_number] = fold_on_row
            else:
                self.paper[folded_row_number] = row
            del self.paper[row_number]
        self.max_y = fold_index - 1

    def fold_on_x_axis(self, fold_index):
        for row_number in range(self.max_y + 1):
            if row_number in self.paper.keys():
                row = self.paper[row_number]
                items_after_fold = [item for item in row if item > fold_index]
                for item in items_after_fold:
                    new_item = fold_index - (item - fold_index)
                    if new_item not in row:
                        row.append(new_item)
                    row.remove(item)
        self.max_x = fold_index - 1

    def print_paper(self):
        result_string = ""
        empty_line = "." * (self.max_x + 1)
        for row_number in range(self.max_y + 1):
            if row_number in self.paper.keys():
                row = self.paper[row_number]
                row_string = ""
                for column_number in range(self.max_x + 1):
                    if column_number in row:
                        row_string += "#"
                    else:
                        row_string += "."
                print(row_string)
                result_string += row_string + "\n"
            else:
                print(empty_line)
                result_string += empty_line + "\n"
        return result_string

if __name__ == "__main__":
    origami = TransparentOrigami()
