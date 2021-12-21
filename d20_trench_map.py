from AoCGui import AoCGui

EXAMPLE_DATA = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""


class TrenchMap(AoCGui):
    def __init__(self):
        super().__init__()
        self.enhancement_algorithm = []
        self.image = []
        self.unlimited_symbol = "."
        self.prepare_gui("Day 20: Trench Map", "Enhance Picture", EXAMPLE_DATA)

    def button_pressed(self):
        self.load_text_box_data()
        self.data_lines.pop()
        # print(self.data_lines)
        if self.part.get() == 1:
            self.part_one()
        else:
            self.part_two()

    def part_one(self):
        self.parse_input()
        print(self.enhancement_algorithm)
        self.print_image()
        for i in range(2):
            print(f"----After {i + 1} enhancements:----------")
            self.enhance_image()
            self.print_image()
            print(self.count_lit_pixels())
        lit_pixels = self.count_lit_pixels()
        self.write_result(f"Number of lit pixels: {lit_pixels}")

    def part_two(self):
        self.parse_input()
        for i in range(50):
            print(f"----After {i + 1} enhancements:----------")
            self.enhance_image()
            print(self.count_lit_pixels())
        lit_pixels = self.count_lit_pixels()
        self.write_result(f"Number of lit pixels: {lit_pixels}")

    def parse_input(self):
        self.data_lines.pop(-1)
        self.enhancement_algorithm = []
        line = self.data_lines.pop(0)
        while line != "":
            self.enhancement_algorithm += list(line)
            line = self.data_lines.pop(0)
        for line in self.data_lines:
            new_image_line = list(line)
            self.image.append(new_image_line)
        self.enlarge_canvas()

    def print_image(self) -> str:
        result = "Image: \n"
        for line in self.image:
            result += "".join(line) + "\n"
        print(result)
        return result

    def enlarge_canvas(self):
        new_canvas = [[self.unlimited_symbol] * len(self.image[0]) + [self.unlimited_symbol, self.unlimited_symbol]]
        new_canvas += [([self.unlimited_symbol] + image_line + [self.unlimited_symbol]) for image_line in self.image]
        new_canvas += [new_canvas[0].copy()]
        self.image = new_canvas

    def enhance_image(self):
        self.enlarge_canvas()
        new_image = [line.copy() for line in self.image]
        for y in range(len(self.image)):
            for x in range(len(self.image[0])):
                binary_list = (self.get_binary_value(x-1, y-1) +
                               self.get_binary_value(x, y-1) +
                               self.get_binary_value(x+1, y-1) +
                               self.get_binary_value(x-1, y) +
                               self.get_binary_value(x, y) +
                               self.get_binary_value(x+1, y) +
                               self.get_binary_value(x-1, y+1) +
                               self.get_binary_value(x, y+1) +
                               self.get_binary_value(x+1, y+1)
                               )
                binary_number = int(binary_list, 2)
                pixel = self.enhancement_algorithm[binary_number]
                new_image[y][x] = pixel
                # print(f"Row {y} Column {x}: {binary_number} becomes {pixel}")
        self.image = new_image
        self.after_care()

    def get_binary_value(self, x, y) -> str:
        if x < 0 or x >= len(self.image[0]) or y < 0 or y >= len(self.image):
            if self.unlimited_symbol == "#":
                return "1"
            else:
                return "0"
        if self.image[y][x] == "#":
            return "1"
        else:
            return "0"

    def count_lit_pixels(self):
        no_lit_pixels = 0
        for line in self.image:
            no_lit_pixels += line.count("#")
        return no_lit_pixels

    def after_care(self):
        if self.enhancement_algorithm[0] == "#":
            if self.unlimited_symbol == ".":
                self.unlimited_symbol = "#"
            else:
                self.unlimited_symbol = "."

if __name__ == "__main__":
    trench_map = TrenchMap()
