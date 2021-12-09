from AoCGui import AoCGui

EXAMPLE_DATA = """acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"""
EXAMPLE_DATA2 = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

SEGMENT_VARIANTS = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9
}

# REVERSE_SEGMENT_VARIANTS = {
#     0: "abcefg",
#     1: "cf",
#     2: "acdeg",
#     3: "acdfg",
#     4: "bcdf",
#     5: "abdfg",
#     6: "abdefg",
#     7: "acf",
#     8: "abcdefg",
#     9: "abcdfg"
# }


class SevenSegmentSearch(AoCGui):
    def __init__(self):
        super().__init__()
        self.prepare_gui("Day 8: Seven Segment Search", "Decode", EXAMPLE_DATA2)

    def button_pressed(self):
        self.load_text_box_data()
        self.data_lines.pop()
        # print(self.data_lines)
        if self.part.get() == 1:
            self.part_one()
        else:
            self.part_two()

    def part_one(self):
        # segment1 = DisplaySegment()
        # segment1.toggle_segments("abdefg")
        # self.write_result(segment1)
        unique_lengths = [2, 3, 4, 7]
        count = 0
        for line in self.data_lines:
            output_values = line.split(" | ")[1]
            outputs = output_values.split(" ")
            print(outputs)
            for output in outputs:
                if len(output) in unique_lengths:
                    count +=1
        self.write_result(f"Digits 1, 4, 7, 8 appear {count} times")

    def part_two(self):
        result = 0
        for line in self.data_lines:
            decoding_values, output_values = line.split(" | ")
            codes = decoding_values.split(" ")
            outputs = output_values.split(" ")
            decoder = self.find_decoder(codes)
            result += self.decode_outputs(outputs, decoder)
        self.write_result(f"Sum of all outputs: {result}")

    def find_decoder(self, codes) -> dict:
        decoder = {}
        to_find = list("abcdefg")
        one = [x for x in codes if len(x) == 2][0]
        len6 = [x for x in codes if len(x) == 6]
        # for i in range(len(to_find)):
        # Finding "c"
        for letter in to_find:
            if letter in one and \
                    (letter not in len6[0] or letter not in len6[1] or letter not in len6[2]):
                decoder[letter] = "c"
                to_find.remove(letter)
                break
        for letter in to_find:
            if letter in one:
                decoder[letter] = "f"
                to_find.remove(letter)
                break
        seven = [x for x in codes if len(x) == 3][0]
        for letter in to_find:
            if letter in seven:
                decoder[letter] = "a"
                to_find.remove(letter)
                break
        four = [x for x in codes if len(x) == 4][0]
        for letter in to_find:
            if letter not in four and \
                    (letter not in len6[0] or letter not in len6[1] or letter not in len6[2]):
                decoder[letter] = "e"
                to_find.remove(letter)
                break
        for letter in to_find:
            if letter not in len6[0] or letter not in len6[1] or letter not in len6[2]:
                decoder[letter] = "d"
                to_find.remove(letter)
                break
        for letter in to_find:
            if letter in four:
                decoder[letter] = "b"
                to_find.remove(letter)
                break
        decoder[to_find[0]] = "g"
        print(decoder)

        return decoder

    def decode_outputs(self, outputs, decoder):
        result = ""
        for output in outputs:
            coded_list = list(output)
            decoded_list = []
            for letter in coded_list:
                decoded_list.append(decoder[letter])
            decoded_list.sort()
            output_number = SEGMENT_VARIANTS["".join(decoded_list)]
            result += str(output_number)
        return int(result)


class DisplaySegment:
    def __init__(self) -> None:
        super().__init__()
        self.segments ={"a": False,
                        "b": False,
                        "c": False,
                        "d": False,
                        "e": False,
                        "f": False,
                        "g": False}

    def toggle_segment(self, name, state=None):
        if state:
            self.segments[name] = state
        else:
            self.segments[name] = not self.segments[name]

    def toggle_segments(self, names: str):
        for name in names:
            self.toggle_segment(name)

    def __repr__(self):
        string_representation = []
        if self.segments["a"]:
            string_representation.append(" ---- ")
        else:
            string_representation.append("      ")
        if self.segments["b"]:
            string_part = "|  "
        else:
            string_part = "   "
        if self.segments["c"]:
            string_part += "  |"
        else:
            string_part += "   "
        string_representation.append(string_part)
        string_representation.append(string_part)
        if self.segments["d"]:
            string_representation.append(" ---- ")
        else:
            string_representation.append("      ")
        if self.segments["e"]:
            string_part = "|  "
        else:
            string_part = "   "
        if self.segments["f"]:
            string_part += "  |"
        else:
            string_part += "   "
        string_representation.append(string_part)
        string_representation.append(string_part)
        if self.segments["g"]:
            string_representation.append(" ---- ")
        else:
            string_representation.append("      ")
        return "\n".join(string_representation)


if __name__ == "__main__":
    seven_segment_search = SevenSegmentSearch()