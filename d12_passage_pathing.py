from AoCGui import AoCGui

EXAMPLE_DATA = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

EXAMPLE_DATA2 = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

EXAMPLE_DATA3 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""


class Path:

    def __init__(self, locations) -> None:
        super().__init__()
        self.locations = locations.copy()
        self.small_cave_visited_twice = False

    def __repr__(self) -> str:
        return " -> ".join(self.locations)

    def add_location(self, location: str):
        # print(f"Adding Location {location} to path {self}, check is {self.small_cave_visited_twice}")
        if location[0].islower() and location in self.locations:
            self.small_cave_visited_twice = True
            # print(f"Small cave was visited twice")
        self.locations.append(location)

    def check_possible_location(self, location: str, version=1) -> bool:
        if version == 1:
            if location[0].isupper() or location not in self.locations:
                return True
            else:
                return False
        else:
            if location[0].isupper() or \
               location not in self.locations or \
                    (location not in ["start", "end"] and not self.small_cave_visited_twice):
                return True
            else:
                return False


class PassagePathing(AoCGui):
    def __init__(self):
        super().__init__()
        self.passages = {}
        self.paths = [Path(["start"])]
        self.complete_paths = []
        self.version = 1
        self.prepare_gui("Day 12: Passage Pathing", "Calculate Paths", EXAMPLE_DATA3)

    def button_pressed(self):
        self.load_text_box_data()
        self.data_lines.pop()
        # print(self.data_lines)

        if self.part.get() == 1:
            self.version = 1
        else:
            self.version = 2
        self.parse_paths()
        # print(self.passages)
        while self.paths:
            path = self.paths.pop(0)
            self.further_path(path)
        self.print_paths()
        self.write_result(f"Number of paths: {len(self.complete_paths)}")

    def parse_paths(self):
        for line in self.data_lines:
            loc1, loc2 = line.split("-")
            if loc1 in self.passages.keys():
                loc1_paths = self.passages[loc1]
                loc1_paths.append(loc2)
                self.passages[loc1] = loc1_paths
            else:
                self.passages[loc1] = [loc2]
            if loc2 in self.passages.keys():
                loc2_paths = self.passages[loc2]
                loc2_paths.append(loc1)
                self.passages[loc2] = loc2_paths
            else:
                self.passages[loc2] = [loc1]

    def further_path(self, path: Path):
        possible_extensions = self.passages[path.locations[-1]]
        for location in possible_extensions:
            if path.check_possible_location(location, version=self.version):
                new_path = Path(path.locations)
                new_path.small_cave_visited_twice = path.small_cave_visited_twice
                new_path.add_location(location)
                if location == "end":
                    self.complete_paths.append(new_path)
                else:
                    self.paths.append(new_path)

    def print_paths(self):
        for path in self.complete_paths:
            print(path)


if __name__ == "__main__":
    passage_pathing = PassagePathing()
