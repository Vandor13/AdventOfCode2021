from AoCGui import AoCGui
import itertools

EXAMPLE_DATA = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""


class Vents(AoCGui):
    def __init__(self):
        super().__init__()
        self.vents = {}
        self.number_of_2_vents = 0
        self.prepare_gui("Day 5: Hydrothermal Venture", "Calculate Vents", EXAMPLE_DATA)

    def button_pressed(self):
        self.load_text_box_data()
        self.data_lines.pop()

        self.vents = {}
        self.number_of_2_vents = 0
        for line in self.data_lines:
            self.determine_line(line)
        self.write_result(f"Number of vents: {self.number_of_2_vents}")

    def determine_line(self, line):
        pos1, pos2 = line.split(" -> ")
        pos1x, pos1y = [int(x) for x in pos1.split(",")]
        pos2x, pos2y = [int(x) for x in pos2.split(",")]
        if pos1y == pos2y:
            x = [pos1x, pos2x]
            x.sort()
            self.horizontal_line(x, pos2y)
        elif pos1x == pos2x:
            y = [pos1y, pos2y]
            y.sort()
            self.vertical_line(pos1x, y)
        else:
            if self.part.get() == 2:
                # print(f"Diagonal line: {line}")
                x = [pos1x, pos2x]
                y = [pos1y, pos2y]
                self.diagonal_line(x, y)

    def horizontal_line(self, x, y):
        for x in range(x[0], x[1]+1):
            self.add_vent(x, y)

    def vertical_line(self, x, y):
        for y in range(y[0], y[1]+1):
            self.add_vent(x, y)

    def diagonal_line(self, x, y):
        if x[0] < x[1]:
            xstep = 1
            xoffset = 1
        else:
            xstep = -1
            xoffset = -1
        if y[0] < y[1]:
            ystep = 1
            yoffset = 1
        else:
            ystep = -1
            yoffset = -1
        for row, column in zip(range(x[0], x[1] + xoffset, xstep), range(y[0], y[1] + yoffset, ystep)):
            # print(f"x: {row} y: {column}")
            self.add_vent(row, column)

    def add_vent(self, row, column):
        position_string = f"{row},{column}"
        print("adding " + position_string)
        number_of_vents = self.vents.get(position_string)
        if number_of_vents:
            if number_of_vents == 1:
                self.number_of_2_vents += 1
            self.vents[position_string] = number_of_vents + 1
        else:
            self.vents[position_string] = 1


if __name__ == "__main__":
    hydro_vents = Vents()
