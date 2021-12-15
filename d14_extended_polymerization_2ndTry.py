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
        self.pairs = dict()  # Saves pairs and their counts
        self.prepare_gui("Day 14: Extended Polymerization", "Calculate Polymerization", EXAMPLE_DATA)

    def button_pressed(self):
        self.load_text_box_data()
        self.data_lines.pop()
        self.parse_input_data()
        # print(f"Polymer: {self.polymer_template}")
        # print(f"Pairs: {self.pair_rules}")
        if self.part.get() == 1:
            self.step_count = 10
            # print(self.polymer_template)
        else:
            self.step_count = 40
        for i in range(self.step_count):
            self.find_new_pairs()
        self.count_elements()

    def find_new_pairs(self):
        print("finding new pairs")
        print(self.pairs)
        pairs_copy = self.pairs.copy()
        for pair in pairs_copy.keys():
            if pair in self.pair_rules.keys():
                occurrences = pairs_copy[pair]
                new_letter = self.pair_rules[pair]
                new_pair_1 = pair[0] + new_letter
                new_pair_2 = new_letter + pair[1]
                self.add_pair(new_pair_1, occurrences)
                self.add_pair(new_pair_2, occurrences)
                # remove the old pairs:
                self.pairs[pair] = self.pairs[pair] - occurrences

    def parse_input_data(self):
        self.polymer_template = self.data_lines[0]
        for pair_string in self.data_lines[2:]:
            key, value = pair_string.split(" -> ")
            self.pair_rules[key] = value
        for i in range(len(self.polymer_template) - 1):
            pair = self.polymer_template[i] + self.polymer_template[i + 1]
            self.add_pair(pair)
        print(self.pairs)

    def count_elements(self):
        element_count = dict()
        for pair in self.pairs.keys():
            occurrences = self.pairs[pair]
            for element in list(pair):
                if element in element_count.keys():
                    element_count[element] = element_count[element] + occurrences
                else:
                    element_count[element] = occurrences
        element_count[self.polymer_template[0]] = element_count[self.polymer_template[0]] + 1
        element_count[self.polymer_template[-1]] = element_count[self.polymer_template[-1]] + 1
        print(element_count)
        counts = [x//2 for x in list(element_count.values())]

        counts.sort()
        self.write_result(f"Result: {counts[-1] - counts[0]}")

    def add_pair(self, pair, amount=1):
        if pair in self.pairs.keys():
            self.pairs[pair] = self.pairs[pair] + amount
        else:
            self.pairs[pair] = amount


if __name__ == "__main__":
    polymerization = Polymerization()
