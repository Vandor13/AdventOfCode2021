from AoCGui import AoCGui
import math

EXAMPLE_DATA = """620080001611562C8802118E34"""


HEX_TRANSLATION = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111"
}


class PacketDecoder(AoCGui):
    def __init__(self):
        super().__init__()
        self.hex_string = ""
        self.bit_string = ""
        self.results = []
        self.version_sum = 0
        self.prepare_gui("Day 16: Packet Decoder", "Decode", EXAMPLE_DATA)

    def button_pressed(self):
        self.load_text_box_data()
        self.data_lines.pop()
        self.bit_string = ""
        self.results = []
        self.version_sum = 0
        self.hex_string = self.data_lines.pop(0)
        # print(self.data_lines)
        if self.part.get() == 1:
            self.part_one()
        else:
            self.part_two()

    def part_one(self):
        self.parse_hex()
        while self.hex_string and int(self.hex_string, 16) != 0:
            print(f"Rest Hex: {self.hex_string}")
            packet_result, packet_length = self.parse_packet()
            self.results.append(packet_result)
        self.write_result(f"Sum of versions: {self.version_sum}\n" +
                          f"Result of transmission: {self.results}")

    def part_two(self):
        pass

    def parse_hex(self):
        bit_string = ""
        for char in self.hex_string:
            bit_string += HEX_TRANSLATION[char]
        print(bit_string)

    def lazy_load_hex(self, number_of_bits):
        while len(self.bit_string) < number_of_bits:
            self.bit_string += HEX_TRANSLATION[self.hex_string[0]]
            self.hex_string = self.hex_string[1:]

    def parse_packet(self):
        version = int(self.get_bits(3), 2)
        self.version_sum += version
        type_id = int(self.get_bits(3), 2)
        if type_id == 4:
            value, number_of_bits = self.parse_literal_value()
            return value, number_of_bits + 6
        else:
            value, number_of_bits = self.parse_operator()
            result = self.parse_value(value, type_id)
            return result, number_of_bits + 6

    def parse_literal_value(self) -> [int, int]:
        number_of_bits = 0
        binary_number = ""
        while True:
            group = self.get_bits(5)
            number_of_bits += 5
            binary_number += group[1:]
            if group[0] == "0":
                break
        result = int(binary_number, 2)
        print(f"Found literal value: {result}")
        # # remove all remaining zeroes
        # self.bit_string = ""
        return [result, number_of_bits]

    def parse_operator(self):
        length_type = self.get_bits(1)
        if length_type == "0":
            total_length = int(self.get_bits(15), 2)
            current_length = 0
            result = []
            while current_length < total_length:
                sub_result, sub_length = self.parse_packet()
                current_length += sub_length
                result.append(sub_result)
            if current_length > total_length:
                print("Error: Read to many bits")
            # # remove all remaining zeroes
            # self.bit_string = ""
            print(f"Found operator: {result}")
            return result, current_length + 16
        else:
            number_subpackages = int(self.get_bits(11), 2)
            print(f"Number of subpackages: {number_subpackages}")
            length = 0
            result = []
            for i in range(number_subpackages):
                sub_result, sub_length = self.parse_packet()
                result.append(sub_result)
                length += sub_length
            # remove all remaining zeroes
            # self.bit_string = ""
            # print(f"Found operator: {result}")
            return result, length + 12

    def get_bits(self, number_of_bits) -> str:
        self.lazy_load_hex(number_of_bits)
        bits = self.bit_string[:number_of_bits]
        if len(self.bit_string) > number_of_bits:
            self.bit_string = self.bit_string[number_of_bits:]
        else:
            self.bit_string = ""
        return bits

    def parse_value(self, value, type_id):
        match type_id:
            case 0:
                return sum(value)
            case 1:
                return math.prod(value)
            case 2:
                return min(value)
            case 3:
                return max(value)
            case 5:
                return 1 if value[0] > value[1] else 0
            case 6:
                return 1 if value[0] < value[1] else 0
            case 7:
                return 1 if value[0] == value[1] else 0



if __name__ == "__main__":
    packet_decoder = PacketDecoder()
