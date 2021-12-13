from AoCGui import AoCGui

EXAMPLE_DATA = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

NUMBER_OF_STEPS = 100
NUMBER_OF_ROWS = 10
NUMBER_OF_COLUMNS = 10


class OctopusPath(AoCGui):
    def __init__(self):
        super().__init__()
        self.dos = []
        self.prepare_gui("Day 11: Dumbo Octopus", "Calculate Flashes", EXAMPLE_DATA)

    def button_pressed(self):
        self.load_text_box_data()
        self.data_lines.pop()

        self.init_octopuses()
        if self.part.get() == 1:
            self.part_one()
        else:
            self.part_two()

    def init_octopuses(self):
        self.dos = []
        for line in self.data_lines:
            row = []
            for energy in list(line):
                row.append(DumboOctopus(int(energy)))
            self.dos.append(row)

    def part_one(self):
        number_of_flashes = 0
        step = 0
        while step < NUMBER_OF_STEPS:
            step += 1
            self.increase_all_octis()
            while self.check_for_pulses():
                pass
            number_of_flashes += self.reset_flashes()
            self.print_octopi()
            print(f"Number of flashes after step {step}: {number_of_flashes}")
        self.write_result(f"Number of flashes after {step} steps: {number_of_flashes}")

    def part_two(self):
        all_flashed = False
        step = 0
        while not all_flashed:
            step += 1
            self.increase_all_octis()
            while self.check_for_pulses():
                pass
            number_of_flashes = self.reset_flashes()
            self.print_octopi()
            print(f"Number of flashes after step {step}: {number_of_flashes}")
            if number_of_flashes == NUMBER_OF_ROWS * NUMBER_OF_COLUMNS:
                all_flashed = True
                print("ALL OCTOPI FLASHED AT THE SAME TIME!")
        self.write_result(f"Number of steps until all octopi flash together: {step}")

    def increase_all_octis(self):
        for row in self.dos:
            for octopus in row:
                octopus.increase_energy()

    def check_for_pulses(self) -> bool:
        pulse_activated = False
        for x in range(NUMBER_OF_COLUMNS):
            for y in range(NUMBER_OF_ROWS):
                if self.dos[x][y].energy_pulse:
                    pulse_activated = True
                    self.increase_all_neighbors(x, y)
                    self.dos[x][y].reset_energy_pulse()
        return pulse_activated

    def increase_all_neighbors(self, x, y):
        for x2 in range(x-1, x+2):
            for y2 in range(y-1, y+2):
                if x2 in range(10) and y2 in range(10):
                    self.dos[x2][y2].increase_energy()

    def reset_flashes(self):
        no_of_flashes = 0
        for row in self.dos:
            for octopus in row:
                if octopus.flashing:
                    no_of_flashes += 1
                    octopus.reset_flashing()
        return no_of_flashes

    def print_octopi(self):
        for row in self.dos:
            print(row)


class DumboOctopus:

    def __init__(self, starting_level=0) -> None:
        super().__init__()
        self.energy = starting_level
        self.flashing = False
        self.energy_pulse = False

    def __repr__(self) -> str:
        return f"'{self.energy}'"

    def increase_energy(self, increase=1):
        if not self.flashing:
            self.energy += increase
            if self.energy > 9:
                self.flashing = True
                self.energy_pulse = True

    def reset_energy_pulse(self):
        self.energy_pulse = False

    def reset_flashing(self):
        self.flashing = False
        self.reset_energy()

    def reset_energy(self):
        self.energy = 0


if __name__ == "__main__":
    octopus_path = OctopusPath()
