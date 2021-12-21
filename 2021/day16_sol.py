from math import prod


def read_input(path):
    with open(path, "r") as f:
        data = f.read()

    return data


class Packet:
    def __init__(self, type_id, version, value):
        self.type_id = type_id
        self.version = version
        self.value = value

    def __call__(self):
        if self.type_id == 4:
            return self.value
        elif self.type_id == 0:
            return sum([v() for v in self.value])
        elif self.type_id == 1:
            return prod([v() for v in self.value])
        elif self.type_id == 2:
            return min([v() for v in self.value])
        elif self.type_id == 3:
            return max([v() for v in self.value])
        elif self.type_id == 5:
            return int(self.value[0]() > self.value[1]())
        elif self.type_id == 6:
            return int(self.value[0]() < self.value[1]())
        elif self.type_id == 7:
            return int(self.value[0]() == self.value[1]())

    def get_sum_of_versions(self):
        if self.type_id == 4:
            return self.version
        else:
            return self.version + sum(
                [v.get_sum_of_versions() for v in self.value]
            )


def hex_to_binary(hex):
    desired = len(hex) * 4
    hex = "0x" + hex
    return f"{int(hex, 16):0>{desired}b}"


def decode_literal(literal):
    value = ""
    bits_read = 0

    while True:
        bits = literal[:5]
        literal = literal[5:]

        value += bits[1:]

        bits_read += 5

        if bits[0] == "0":
            break

    return bits_read, int(value, 2)


def decode_subpackets(packet, length, in_bits):
    bits_read = 0

    read, value = decode_packet(packet)
    value = [value]

    bits_read += read

    br = None
    new_value = None

    if in_bits:
        if read < length:
            br, new_value = decode_subpackets(
                packet[read:], length - read, in_bits
            )
    else:
        if length - 1 > 0:
            br, new_value = decode_subpackets(
                packet[read:], length - 1, in_bits
            )

    if new_value:
        value += new_value
        bits_read += br

    return bits_read, value


def decode_packet(packet):
    version = int(packet[:3], 2)
    type_id = int(packet[3:6], 2)

    bits_read = 6

    if type_id == 4:
        literal = packet[6:]
        read, value = decode_literal(literal)
    else:
        length_type = packet[6]
        if length_type == "0":
            length = int(packet[7:22], 2)
            bits_read += 16
            packet = packet[22:]
        else:
            length = int(packet[7:18], 2)
            bits_read += 12
            packet = packet[18:]
        read, value = decode_subpackets(packet, length, length_type == "0")
    bits_read += read
    out = Packet(type_id, version, value)

    return bits_read, out


packet = read_input("day16").strip()
_, data = decode_packet(hex_to_binary(packet))

# Part 1

print(f"Sum of versions: {data.get_sum_of_versions()}")

# Part 2

print(f"Expression evaluates to: {data()}")
