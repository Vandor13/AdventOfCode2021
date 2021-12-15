from AoCGui import AoCGui

EXAMPLE_DATA = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""
NUMBER_OF_DAYS = 256


class Chiton(AoCGui):
    def __init__(self):
        super().__init__()
        self.map = []
        self.map_size = 0
        self.paths = {} # Right now: Saves length of path as key and path as value
        self.path_to_goal = None
        self.best_sub_paths = dict()
        self.prepare_gui("Day 15: Chiton", "Calculate Route", EXAMPLE_DATA)

    def button_pressed(self):
        self.load_text_box_data()
        self.data_lines.pop()
        # print(self.data_lines)
        if self.part.get() == 1:
            self.parse_map()
            self.calculate_path()
        else:
            self.parse_bigger_map()
            self.print_map()
            self.calculate_path()

    def calculate_path(self):
        # Add starting point as first path
        self.paths = {0: [[[0, 0]]]}
        self.best_sub_paths[(0, 0)] = 0
        while self.find_next_paths():
            continue
        self.write_result(f"Best path found with risk: {self.path_to_goal[0]}")

    def parse_map(self):
        for line in self.data_lines:
            parsed_line = [int(x) for x in list(line)]
            self.map.append(parsed_line)
        self.map_size = len(self.map)

    def parse_bigger_map(self):
        for line in self.data_lines:
            big_line = []
            for i in range(5):
                parsed_line = [int(x) + i if int(x) + i < 10 else int(x) + i - 9 for x in list(line)]
                big_line = big_line + parsed_line
            self.map.append(big_line)
        base_rows = self.map.copy()
        for i in range(1, 5):
            for row in base_rows:
                new_line = [x + i if x + i < 10 else x + i - 9 for x in row]
                self.map.append(new_line)
        self.map_size = len(self.map)

    def find_next_paths(self) -> bool:
        lowest_risk = min(list(self.paths.keys()))
        print(f"new lowest risk: {lowest_risk}")
        if self.path_to_goal and self.path_to_goal[0] <= lowest_risk:
            return False
        paths = self.paths[lowest_risk]
        print(f"Looking at {len(paths)} possible paths")
        # print(paths)
        self.paths.pop(lowest_risk)
        for path in paths:
            self.add_new_paths(path, lowest_risk)
        return True

    def add_new_paths(self, path, current_risk):
        x, y = path[-1]
        # moving to the right
        if x < self.map_size - 1:
            self.add_path(path, x + 1, y, current_risk)
        # moving down
        if y < self.map_size - 1:
            self.add_path(path, x, y + 1, current_risk)
        # moving left
        if x > 0:
            self.add_path(path, x - 1, y, current_risk)
        # moving up
        if y > 0:
            self.add_path(path, x, y - 1, current_risk)

    def add_path(self, path, x, y, current_risk):
        # only enhance the path if we don't go to an already visited field
        if [x, y] not in path:
            new_risk = current_risk + self.map[y][x]
            new_path = path.copy()
            new_path.append([x, y])
            # check if a better subpath to the new point was already found
            if (x, y) in self.best_sub_paths.keys() and self.best_sub_paths[(x, y)] <= new_risk:
                return
            else:
                self.best_sub_paths[(x, y)] = new_risk
            if new_risk in self.paths.keys():
                self.paths[new_risk].append(new_path)
            else:
                self.paths[new_risk] = [new_path]
            if x == self.map_size - 1 and y == self.map_size - 1:
                if not self.path_to_goal or self.path_to_goal[0] > new_risk:
                    print(f"Found goal with path of risk {new_risk}!")
                    self.path_to_goal = (new_risk, new_path)

    def print_map(self):
        print("Print out of the map:")
        for line in self.map:
            print(" ".join([str(x) for x in line]))


if __name__ == "__main__":
    chiton = Chiton()
