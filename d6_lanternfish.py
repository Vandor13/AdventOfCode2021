from AoCGui import AoCGui

EXAMPLE_DATA = """3,4,3,1,2"""
NUMBER_OF_DAYS = 256


class Lanternfish(AoCGui):
    def __init__(self):
        super().__init__()
        self.no_of_fishies = 0
        self.fishies = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        self.immature_fishies = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        self.day = 0
        self.prepare_gui("Day 6: Lanternfish", "Calculate Fishies", EXAMPLE_DATA)

    def button_pressed(self):
        self.no_of_fishies = 0
        self.fishies = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        self.immature_fishies = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        self.day = 0
        self.load_text_box_data()
        self.data_lines.pop()
        # print(self.data_lines)
        if self.part.get() == 1:
            self.part_one()
        else:
            self.part_two()

    def part_one(self):
        initial_fishies = [int(x) for x in self.data_lines[0].split(",")]
        self.init_fishies(initial_fishies)
        for i in range(NUMBER_OF_DAYS):
            self.process_day()
        number_of_fishies = sum(self.fishies.values()) + sum(self.immature_fishies.values())
        result_string = f"After {NUMBER_OF_DAYS} days we have {number_of_fishies} fishies"
        self.write_result(result_string)

    def part_two(self):
        pass

    def init_fishies(self, fishies):
        for fish in fishies:
            number_of_fishies = self.fishies.get(fish)
            self.fishies[fish] = number_of_fishies + 1
        print(self.fishies)

    def process_day(self):
        number_of_fishies = self.fishies.get(self.day)

        matured_fishies = self.immature_fishies.get(self.day)
        self.immature_fishies[self.day] = 0

        # Add new immature fishies to day + 2
        self.immature_fishies[(self.day + 2) % 7] = number_of_fishies

        # Add now mature fishies on the current day
        self.fishies[self.day] = number_of_fishies + matured_fishies

        number_of_fishies = sum(self.fishies.values()) + sum(self.immature_fishies.values())
        print(f"On day {self.day} we have {number_of_fishies} fishes")

        self.day = (self.day + 1) % 7


if __name__ == "__main__":
    lanternfish = Lanternfish()
