from AoCGui import AoCGui
import statistics

EXAMPLE_DATA = """16,1,2,0,4,2,7,1,2,14"""


class CrabAlignment(AoCGui):
    def __init__(self):
        super().__init__()
        self.positions = []
        self.best_position = None
        self.best_fuel_need = None
        self.prepare_gui("Day 7: The Treachery of Whales", "Calculate Best Position", EXAMPLE_DATA)

    def button_pressed(self):
        self.load_text_box_data()
        self.data_lines.pop()
        # print(self.data_lines)
        self.find_best_fuel()

    def find_best_fuel(self):
        self.positions = [int(x) for x in self.data_lines[0].split(",")]
        print(self.positions)
        start_position = int(statistics.mean(self.positions))
        self.best_position = self.find_local_minimum(start_position)
        self.best_fuel_need = self.calculate_fuel_need(self.best_position)

        result_string = (f"Best position: {self.best_position}\n"
                         f"Fuel need: {self.best_fuel_need}")
        self.write_result(result_string)

    def calculate_fuel_need(self, goal_position):
        fuel_need = 0
        for position in self.positions:
            if self.part.get() == 1:
                distance = abs(position - goal_position)
                fuel_need += distance
            else:
                distance = abs(position - goal_position)
                fuel_need += distance * (distance + 1) // 2
        return fuel_need

    def find_local_minimum(self, start_position) -> int:
        current_position = start_position
        current_fuel_need = self.calculate_fuel_need(current_position)
        new_position = None
        while current_position != new_position:
            if new_position != None:
                current_position = new_position
                current_fuel_need = self.calculate_fuel_need(current_position)
            else:
                new_position = current_position
            if self.calculate_fuel_need(current_position + 1) < current_fuel_need:
                new_position = current_position + 1
                continue
            elif current_position >= 0 and self.calculate_fuel_need(current_position - 1) < current_fuel_need:
                new_position = current_position - 1
        return current_position


if __name__ == "__main__":
    crab_alignment = CrabAlignment()
