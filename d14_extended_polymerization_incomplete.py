from AoCGui import AoCGui

EXAMPLE_DATA = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


class Polymerization(AoCGui):
    def __init__(self):
        super().__init__()
        self.polymer_template = ""
        self.step_count = 10
        self.pair_rules = dict()
        self.additions = dict()  # Saves already calculated additions
        self.prepare_gui("Day 14: Extended Polymerization", "Calculate Polymerization", EXAMPLE_DATA)

    def button_pressed(self):
        self.load_text_box_data()
        self.data_lines.pop()
        self.parse_input_data()
        # print(f"Polymer: {self.polymer_template}")
        # print(f"Pairs: {self.pair_rules}")
        if self.part.get() == 1:
            self.step_count = 10
            self.reinforce_v2()
            print(self.polymer_template)
        else:
            self.step_count = 40
            self.reinforce_v2()

    def reinforce(self):
        print(f"Starting Polymer: {self.polymer_template}")
        for i in range(self.step_count):
            print(f"Executing step {i + 1}")
            self.replace_polymer()
            # print(f"After step {i+1}: {self.polymer_template}")
        self.count_elements()

    def part_two(self):
        pass

    def parse_input_data(self):
        self.polymer_template = self.data_lines[0]
        for pair_string in self.data_lines[2:]:
            key, value = pair_string.split(" -> ")
            self.pair_rules[key] = value

    def replace_polymer(self):
        new_polymer = ""
        for i in range(len(self.polymer_template) - 1):
            new_polymer += self.polymer_template[i]
            pair = self.polymer_template[i] + self.polymer_template[i + 1]
            # Do polymer insertion if pair is in rules
            if pair in self.pair_rules.keys():
                new_polymer += self.pair_rules[pair]
        new_polymer += self.polymer_template[-1]
        self.polymer_template = new_polymer

    def reinforce_v2(self):
        print(f"Starting Polymer: {self.polymer_template}")
        new_polymer = ""
        for i in range(len(self.polymer_template) - 1):
            print(f"Processing index {i}")
            new_polymer += self.polymer_template[i]
            pair = self.polymer_template[i] + self.polymer_template[i + 1]
            new_polymer += self.find_additions(pair, self.step_count)
        new_polymer += self.polymer_template[-1]
        self.polymer_template = new_polymer
        self.count_elements()

    def count_elements(self):
        element_count = dict()
        for element in self.polymer_template:
            if element in element_count.keys():
                element_count[element] = element_count[element] + 1
            else:
                element_count[element] = 1
        print(element_count)
        counts = list(element_count.values())
        counts.sort()
        self.write_result(f"Result: {counts[-1] - counts[0]}")

    def find_additions(self, pair, steps) -> tuple:
        print(f"Processing step {steps}")
        if pair in self.pair_rules.keys():
            already_calculated, calculated_steps = self.find_already_calculated_addition(pair, steps)
            if already_calculated:
                return already_calculated, calculated_steps
            new_letter = self.pair_rules[pair]
            if steps > 1:
                front, front_completed = self.find_additions(pair[0] + new_letter, steps - 1)
                back, back_completed = self.find_additions(new_letter + pair[1], steps - 1)
                new_addition = front + new_letter + back
                if front_completed and back_completed:
                    completed = max(front_completed, back_completed) + 1
                else:
                    completed = None
                self.save_already_calculated_addition(pair, steps, new_addition, completed)
                return new_addition, completed
            else:
                self.save_already_calculated_addition(pair, steps, new_letter, steps)
                return new_letter, 1
        else:
            return "", True

    def find_already_calculated_addition(self, pair, steps):
        if pair in self.additions.keys():
            step_dict, complete_at = self.additions[pair]
            if complete_at and steps <= complete_at:
                return step_dict[steps], complete_at
            elif steps in step_dict.keys():
                return step_dict[steps], steps
            else:
                return None, None
        else:
            return None, None

    def save_already_calculated_addition(self, pair, steps, addition, complete_steps):
        if pair in self.additions.keys():
            step_dict, complete_at = self.additions[pair]
            step_dict[steps] = addition
            if complete_steps and complete_at and complete_steps < complete_at:
                self.additions[pair] = (step_dict, complete_steps)
            else:
                self.additions[pair] = (step_dict, complete_at)
        else:
            self.additions[pair] = ({
                steps: addition
            }, None)


if __name__ == "__main__":
    polymerization = Polymerization()
