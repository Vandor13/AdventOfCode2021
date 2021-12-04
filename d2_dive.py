from AoCGui import AoCGui

EXAMPLE_DATA= """forward 5
down 5
forward 8
up 3
down 8
forward 2"""

class Dive(AoCGui):
    def __init__(self):
        super().__init__()
        self.horizontal_position = 0
        self.depth = 0
        self.aim = 0
        self.prepare_gui("Day 2: Dive!", "Calculate Position", EXAMPLE_DATA)

    def button_pressed(self):
        super().button_pressed()
        self.plot_course()

    def plot_course(self):
        self.horizontal_position = 0
        self.depth = 0
        self.aim = 0
        commands = [command.split(" ") for command in self.data_lines]
        # print(commands)
        if self.part.get() == 1:
            for command in commands:
                self.execute_command(command)
        else:
            print("Part 2")
            for command in commands:
                self.execute_command_with_aim(command)
        result = self.horizontal_position * self.depth
        text = f"""Horizontal Position: {self.horizontal_position}
        Depth: {self.depth}
        Result: {result}"""
        self.write_result(text)

    def execute_command(self, command):
        match command[0]:
            case "forward":
                self.horizontal_position += int(command[1])
            case "down":
                self.depth += int(command[1])
            case "up":
                self.depth -= int(command[1])

    def execute_command_with_aim(self, command):
        match command[0]:
            case "forward":
                print(f"forward {command[1]}")
                print(f"Hor: {self.horizontal_position}")
                self.horizontal_position += int(command[1])
                self.depth += self.aim * int(command[1])
            case "down":
                self.aim += int(command[1])
            case "up":
                self.aim -= int(command[1])


if __name__ == "__main__":
    dive = Dive()
