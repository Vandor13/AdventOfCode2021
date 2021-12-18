from AoCGui import AoCGui

EXAMPLE_DATA = """target area: x=20..30, y=-10..-5"""


class TrickShot(AoCGui):
    def __init__(self):
        super().__init__()
        self.x_range = []
        self.y_range = []
        self.best_steps = 0
        self.best_x = None
        self.best_y = None
        self.highest_y = 0
        self.prepare_gui("Day 17: Trick Shot", "Calculate Shot", EXAMPLE_DATA)

    def button_pressed(self):
        self.load_text_box_data()
        self.data_lines.pop()
        self.parse_data()
        # print(self.data_lines)
        if self.part.get() == 1:
            self.part_one()
        else:
            self.part_two()

    def part_one(self):
        # self.find_best_x()
        # for steps in range(self.best_steps - 2, self.best_steps + 3):
        #     self.find_best_y(steps)
        self.brute_force()
        self.write_result(f"Best velocity: ({self.best_x}, {self.best_y}) with highest y: {self.highest_y}")

    def part_two(self):
        pass

    def parse_data(self):
        target_area_string = self.data_lines.pop(0).split("area: ")[1]
        target_x, target_y = target_area_string.split(", ")
        low_x, high_x = [int(x) for x in target_x[2:].split("..")]
        low_y, high_y = [int(y) for y in target_y[2:].split("..")]
        print(f"Low X: {low_x}, High X: {high_x}")
        print(f"Low Y: {low_y}, High Y: {high_y}")
        self.x_range = range(low_x, high_x + 1)
        self.y_range = range(low_y, high_y + 1)

    def find_best_x(self):
        best_x, best_steps = 0, 0
        endpoint = max(self.x_range)
        for x in range(1, min(self.x_range)):
            vx = x
            posx = 0
            steps = 0
            while vx > 0 and posx < endpoint:
                posx += vx
                vx -= 1
                steps += 1
                if posx in self.x_range:
                    if best_steps < steps:
                        best_steps = steps
                        best_x = x
        self.best_steps = best_steps
        self.best_x = best_x
        print(f"Best number of steps: {best_steps} with initial x velocity: {best_x}")

    def find_best_y(self, no_of_steps):
        best_y, max_y = 0, 0
        lowest_point = min(self.y_range)
        for y in range(1, abs(lowest_point) * 4):
            vy = y
            posy = 0
            highest_y = 0
            for steps in range(no_of_steps):
                posy += vy
                vy -= 1
                if posy > highest_y:
                    highest_y = posy
                if posy < lowest_point:
                    break
            if posy in self.y_range and highest_y > max_y:
                best_y = y
                max_y = highest_y
        if max_y > self.highest_y:
            self.best_y = best_y
            self.highest_y = max_y

    def brute_force(self):
        bestx, besty = 0, 0
        highest_y = 0
        for x in range(50):
            for y in range(50):
                steps = 0
                posx, posy = 0, 0
                vx, vy = x, y
                local_highest_y = 0
                hit = False
                while posx < max(self.x_range) and (vy > 0 or posy > min(self.y_range)) and (vx > 0 or posx in self.x_range):
                    posx += vx
                    if vx > 0:
                        vx -= 1
                    posy += vy
                    if posy > local_highest_y:
                        local_highest_y = posy
                    vy -= 1
                    if posx in self.x_range and posy in self.y_range:
                        hit = True
                if hit:
                    print(f"Hit: ({x}, {y}) with highest y: {local_highest_y}")
                if hit and local_highest_y > highest_y:
                    bestx = x
                    besty = y
                    highest_y = local_highest_y
        self.best_x = bestx
        self.best_y = besty
        self.highest_y = highest_y


if __name__ == "__main__":
    trickshot = TrickShot()
