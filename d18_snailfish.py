from AoCGui import AoCGui

EXAMPLE_DATA = """[[[[[9,8],1],2],3],4]"""


class Snailfish(AoCGui):
    def __init__(self):
        super().__init__()
        self.snailfish_numbers = []
        self.prepare_gui("Day 18: Snailfish", "Calculate Homework", EXAMPLE_DATA)

    def button_pressed(self):
        print("-" * 20)
        self.load_text_box_data()
        self.data_lines.pop()
        self.snailfish_numbers = []
        self.parse_data()
        self.print_snailfish_number()
        if self.part.get() == 1:
            self.part_one()
        else:
            self.part_two()

    def part_one(self):
        while len(self.snailfish_numbers) > 1:
            self.addition()
            self.reduce()
        print(self.snailfish_numbers)
        magnitude = self.calculate_magnitude()
        self.write_result(f"Final sum: {self.print_snailfish_number()}\n Magnitude: {magnitude}")

    def part_two(self):
        highest_magnitude = 0
        copy_of_numbers = self.snailfish_numbers.copy()
        for i in range(len(copy_of_numbers)):
            for j in range(len(copy_of_numbers)):
                if i == j:
                    continue
                self.snailfish_numbers = [copy_of_numbers[i].copy(), copy_of_numbers[j].copy()]
                while len(self.snailfish_numbers) > 1:
                    self.addition()
                    self.reduce()
                magnitude = self.calculate_magnitude()
                if magnitude > highest_magnitude:
                    highest_magnitude = magnitude
        self.write_result(f"Highest Magnitude: {highest_magnitude}")

    def reduce(self, number_index=0):
        while True:
            if self.explode(number_index):
                continue
            elif self.split(number_index):
                continue
            break

    def addition(self, index_a=0, index_b=1):
        second_number = self.snailfish_numbers.pop(index_b)
        first_number = self.snailfish_numbers.pop(index_a)
        new_number = ["["] + first_number + [","] + second_number + ["]"]
        self.snailfish_numbers.insert(index_a, new_number)

    def explode(self, number_index=0) -> bool:
        exploded = False
        number = self.snailfish_numbers[number_index]
        index = self.find_fourtimes_nested_number(number)
        if index:
            exploded = True
            pair = number[index - 1: index + 4]
            left_rest = number[:index - 1]
            right_rest = number[index + 4:]
            self.add_on_rightmost(left_rest, pair[1])
            self.add_on_leftmost(right_rest, pair[3])
            self.snailfish_numbers[number_index] = left_rest + [0] + right_rest
        return exploded

    def find_fourtimes_nested_number(self, number: list):
        number_of_opening_brackets = 0
        for index in range(len(number)):
            element = number[index]
            if isinstance(element, int) and number_of_opening_brackets >= 5 and isinstance(number[index + 2], int):
                return index
            elif not isinstance(element, int) and element == "[":
                number_of_opening_brackets += 1
            elif not isinstance(element, int) and element == "]":
                number_of_opening_brackets -= 1
        return False

    def split(self, number_index=0) -> bool:
        number = self.snailfish_numbers[number_index]
        for index in range(len(number)):
            if isinstance(number[index], int) and number[index] > 9:
                value = number.pop(index)
                first_number = value // 2
                second_number = value - first_number
                new_pair = ["[", first_number, ",", second_number, "]"]
                self.snailfish_numbers[number_index] = number[:index] + new_pair + number[index:]
                return True # split was done
        return False # no split done

    def parse_data(self):
        if self.data_lines[-1] == "":
            self.data_lines.pop(-1)
        for number_string in self.data_lines:
            number = [int(x) if x.isnumeric() else x for x in number_string ]
            self.snailfish_numbers.append(number)

    def add_on_rightmost(self, number, value):
        for index in range(len(number) - 1, 0, -1):
            if isinstance(number[index], int):
                number[index] += value
                return

    def add_on_leftmost(self, number, value):
        for index in range(len(number)):
            if isinstance(number[index], int):
                number[index] += value
                return

    def print_snailfish_number(self):
        for number in self.snailfish_numbers:
            strings = [str(x) if isinstance(x, int) else x for x in number]
            result = "".join(strings)
            print(result)
            return result

    def calculate_magnitude(self):
        number = self.snailfish_numbers[0]
        while len(number) > 1:
            for index in range(len(number)):
                if isinstance(number[index], int) and isinstance(number[index + 2], int):
                    magnitude = number[index] * 3 + number[index + 2] * 2
                    if len(number) > 5:
                        number = number[:index - 1] + [magnitude] + number[index + 4:]
                    else:
                        number = [magnitude]
                    break
        print(f"Magnitude: {number[0]}")
        return number[0]


if __name__ == "__main__":
    snailfish = Snailfish()
