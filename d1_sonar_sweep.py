from AoCGui import AoCGui

EXAMPLE_DATA = """199
200
208
210
200
207
240
269
260
263"""

class SonarSweep(AoCGui):
    def __init__(self):
        super().__init__()
        self.prepare_gui("Day 1: Sonar Sweep", "Calculate Depth Change", EXAMPLE_DATA)

    def button_pressed(self):
        self.load_text_box_data()
        self.data_lines.pop()
        if self.part.get() == 1:
            self.calculate_no_of_increases()
        else:
            self.calculate_no_of_window_increases()

    def calculate_no_of_increases(self):
        last_depth = ""
        no_of_increases = 0
        for depth in [int(x) for x in self.data_lines]:
            if last_depth != "":
                if depth > last_depth:
                    no_of_increases += 1
            last_depth = depth
        self.write_result(no_of_increases)

    def calculate_no_of_window_increases(self):
        first_depth = int(self.data_lines.pop(0))
        second_depth = int(self.data_lines.pop(0))
        windows = []
        last_windows = [first_depth + second_depth, second_depth]
        for depth in [int(x) for x in self.data_lines]:
            windows.append(last_windows.pop(0) + depth)
            last_windows[0] = last_windows[0] + depth
            last_windows.append(depth)

        # print(windows)

        no_of_increases = 0
        last_depth = ""
        for depth in windows:
            if last_depth != "":
                if depth > last_depth:
                    no_of_increases += 1
            last_depth = depth
        self.write_result(no_of_increases)


if __name__ == "__main__":
    sonar_sweep = SonarSweep()
