from AoCGui import AoCGui

EXAMPLE_DATA = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

SCORES = {")": 3,
          "]": 57,
          "}": 1197,
          ">": 25137}

PAIRS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}

COMPLETION_SCORES = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4
}

class SyntaxScoring(AoCGui):
    def __init__(self):
        super().__init__()
        self.completion_scores = []
        self.prepare_gui("Day 10: Syntax Scoring", "Calculate Risk", EXAMPLE_DATA)

    def button_pressed(self):
        self.load_text_box_data()
        self.data_lines.pop()
        if self.part.get() == 1:
            self.part_one()
        else:
            self.part_two()

    def part_one(self):
        score = 0
        for line in self.data_lines:
            score += self.check_for_corruption(line)
        self.write_result(f"Syntax Error Score: {score}")

    def check_for_corruption(self, line):
        elements = list(line)
        opened_brackets = []
        for element in elements:
            if element in PAIRS.keys():
                opened_brackets.append(element)
            elif PAIRS[opened_brackets.pop(-1)] != element:
                if element in SCORES.keys():
                    return SCORES[element]
                else:
                    self.score_brackets(opened_brackets)
                    return 0 # incomplete row
        self.score_brackets(opened_brackets)
        return 0 # Either no error or incomplete

        while brackets:
            score *= 5
            bracket = brackets.pop(-1)
            score += COMPLETION_SCORES[bracket]
        self.completion_scores.append(score)

    def part_two(self):
        self.completion_scores = []
        for line in self.data_lines:
            self.check_for_corruption(line)
        self.completion_scores.sort()
        print(self.completion_scores)
        winning_score = self.completion_scores[len(self.completion_scores) // 2]
        self.write_result(f"Syntax Error Score: {winning_score}")


if __name__ == "__main__":
    syntax_scorer = SyntaxScoring()
