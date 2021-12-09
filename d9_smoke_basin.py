from AoCGui import AoCGui

EXAMPLE_DATA = """2199943210
3987894921
9856789892
8767896789
9899965678"""


class SmokeBasin(AoCGui):
    def __init__(self):
        super().__init__()
        self.heatmap = []
        self.height = 0
        self.width = 0
        self.prepare_gui("Day 9: Smoke Basin", "Calculate Risk", EXAMPLE_DATA)

    def button_pressed(self):
        self.heatmap = []
        self.height = 0
        self.width = 0
        self.load_text_box_data()
        self.data_lines.pop()
        # print(self.data_lines)
        self.parse_heatmap()
        self.height = len(self.heatmap)
        self.width = len(self.heatmap[0])
        if self.part.get() == 1:
            self.part_one()
        else:
            self.part_two()

    def part_one(self):
        risk = 0
        baisin_points = self.find_local_minimums()
        for point in baisin_points:
            risk += self.heatmap[point[0]][point[1]] + 1
        self.write_result(f"Total risk: {risk}")

    def find_local_minimums(self):
        local_minimums = []
        for x in range(self.width):
            for y in range(self.height):
                value = self.heatmap[y][x]
                neighbours = self.get_neighbours(y, x)
                local_minimum = True
                for neighbour in neighbours:
                    if self.heatmap[neighbour[0]][neighbour[1]] <= value:
                        local_minimum = False
                        break
                if local_minimum:
                    local_minimums.append((y, x))
        return local_minimums

    def part_two(self):
        baisin_points = self.find_local_minimums()
        baisin_sizes = []
        for point in baisin_points:
            baisin_sizes.append(self.calculate_baisin_size(point))
        print(baisin_sizes)
        baisin_sizes.sort(reverse=True)
        result = baisin_sizes[0] * baisin_sizes[1] * baisin_sizes[2]
        self.write_result(f"Sum of 3 biggest baisin sizes: {result}")

    def parse_heatmap(self):
        for line in self.data_lines:
            parsed_line = [int(x) for x in list(line)]
            self.heatmap.append(parsed_line)

    def get_neighbours(self, y, x):
        neighbours = []
        if y > 0:
            neighbours.append((y-1, x))
        if y < self.height - 1:
            neighbours.append((y+1, x))
        if x > 0:
            neighbours.append((y, x-1))
        if x < self.width - 1:
            neighbours.append((y, x+1))
        return neighbours

    def calculate_baisin_size(self, search_point):
        to_search = [search_point]
        searched_points = []
        baisin_size = 0
        while to_search:
            current_point = to_search.pop()
            searched_points.append(current_point)
            baisin_size +=1
            neighbours = self.get_neighbours(current_point[0], current_point[1])
            for neighbour in neighbours:
                if neighbour not in searched_points and neighbour not in to_search \
                        and self.heatmap[neighbour[0]][neighbour[1]] < 9:
                    to_search.append(neighbour)
        return baisin_size


if __name__ == "__main__":
    smoke_basin = SmokeBasin()
