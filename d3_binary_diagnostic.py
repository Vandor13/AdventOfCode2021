from AoCGui import AoCGui

EXAMPLE_DATA = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""


class Diagnostics(AoCGui):
    def __init__(self):
        super().__init__()
        self.gamma_rate = 0
        self.epsilon_rate = 0
        self.power_consumption = 0
        self.oxygen_generator_rating = 0
        self.co2_scrubber_rating = 0
        self.numbers = []
        self.prepare_gui("Day 3: Binary Diagnostics", "Calculate Rates", EXAMPLE_DATA)

    def button_pressed(self):
        super().button_pressed()
        self.calculate_power_consumption()

        #self.interpret_datalines_as_ints()
        #self.numbers.sort()

        self.calculate_oxygen_generator_rating()
        self.calculate_co2_scrubber_rating()
        multiplication = self.oxygen_generator_rating * self.co2_scrubber_rating

        result_text = f"""Gamma Rate: {bin(self.gamma_rate)} or {self.gamma_rate}
Epsilon Rate: {bin(self.epsilon_rate)} or {self.epsilon_rate}
Power Consumption: {self.power_consumption}
Oxygen Generator Rating: {self.oxygen_generator_rating}
CO2 Scrubber Rating: {self.co2_scrubber_rating}
Multiplied: {multiplication}"""
        self.write_result(result_text)

    def calculate_power_consumption(self):
        self.gamma_rate = 0b0
        self.epsilon_rate = 0b0
        self.power_consumption = 0

        self.calculate_gamma_rate()
        self.power_consumption = self.gamma_rate * self.epsilon_rate
        # self.calculate_epsilon_rate()

        # print(len(self.data_lines[0]))
        # print(self.data_lines)

    def calculate_gamma_rate(self):
        number_of_data = len(self.data_lines)
        lenght_of_numbers = (len(self.data_lines[0]))
        # print(number_of_data)
        digits = [0] * lenght_of_numbers
        # print(digits)
        for date in self.data_lines:
            for i in range(lenght_of_numbers):
                if date[i] == "1":
                    digits[i] += 1

        bin_gamma_string = "0b"
        bin_epsilon_string = "0b"
        for digit in digits:
            if digit * 2 > number_of_data:
                bin_gamma_string = bin_gamma_string + "1"
                bin_epsilon_string = bin_epsilon_string + "0"
            else:
                bin_gamma_string = bin_gamma_string + "0"
                bin_epsilon_string = bin_epsilon_string + "1"
        # print(bin_gamma_string)
        self.gamma_rate = int(bin_gamma_string, 2)
        self.epsilon_rate = int(bin_epsilon_string, 2)

    # def calculate_epsilon_rate(self):
    #     self.epsilon_rate = ~self.gamma_rate

    def calculate_oxygen_generator_rating(self):
        numbers = [[list(string), string] for string in self.data_lines]
        # print("Numbers start as:")
        # print(numbers)
        while len(numbers) > 1:
            numbers = reduce_list(numbers, "oxygen")
            # print("Reduced list to:")
            # print(numbers)
        bin_string = "0b" + numbers[0][1]
        self.oxygen_generator_rating = int(bin_string, 2)

    def calculate_co2_scrubber_rating(self):
        numbers = [[list(string), string] for string in self.data_lines]
        # print("Numbers start as:")
        # print(numbers)
        while len(numbers) > 1:
            numbers = reduce_list(numbers, "co2")
            # print("Reduced list to:")
            # print(numbers)
        bin_string = "0b" + numbers[0][1]
        self.co2_scrubber_rating = int(bin_string, 2)


def reduce_list(numbers: list, mode: str) -> list:
    list_zero = []
    list_one = []
    for number in numbers:
        # print(number)
        # print(number[0])
        if number[0][0] == "0":
            number[0].pop(0)
            list_zero.append([number[0], number[1]])
        else:
            number[0].pop(0)
            list_one.append([number[0], number[1]])
    if len(list_zero) > len(list_one):
        if mode == "oxygen":
            return list_zero
        else:
            return list_one
    else:
        if mode == "oxygen":
            return list_one
        else:
            return list_zero



    # def calculate_oxygen_generator_rating(self):
    #     # Theory: All the explanation in part 2 burns down to:
    #     # Find the closest (but only lower) number to the gamma rating
    #
    #     absolute_difference_function = lambda list_value: abs(list_value - self.gamma_rate)
    #
    #     closest_value = min(self.numbers, key=absolute_difference_function)
    #
    #     self.oxygen_generator_rating = closest_value
    #
    # def calculate_co2_scrubber_rating(self):
    #     # Theory: All the explanation in part 2 burns down to:
    #     # Find the closest (but only lower) number to the epsilon rating
    #     # self.co2_scrubber_rating = self.find_closest_number(self.epsilon_rate)
    #     pass
    #
    # def interpret_datalines_as_ints(self):
    #     for binary in self.data_lines:
    #         bin_string = "0b" + binary
    #         number = int(bin_string, 2)
    #         self.numbers.append(number)


if __name__ == "__main__":
    diagnostics = Diagnostics()
