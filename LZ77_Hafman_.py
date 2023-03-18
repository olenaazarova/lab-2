import heapq
from typing import List


class LZ77HuffmanEncoder:
    def __init__(self, window_size = 64, lookahead_buffer_size=16):
        self.window_size = window_size
        self.lookahead_buffer_size = lookahead_buffer_size
        self.bitstream = ""
        self.huffman_table = {}

    def encode(self, data: str) -> str:
        index = 0
        while index < len(data):
            match_length, match_offset = self.find_longest_match(data, index)
            if match_length == 0:
                self.bitstream += "0" + bin(ord(data[index]))[2:].zfill(8)
                index += 1
            else:
                self.bitstream += "1" + bin(match_length)[2:].zfill(4) + bin(match_offset)[2:].zfill(12)
                index += match_length

        self.huffman_table = {}
        for char in set(self.bitstream):
            self.huffman_table[char] = self.bitstream.count(char) / len(self.bitstream)
        self.huffman_table = self.build_huffman_tree(self.huffman_table)
        self.bitstream = self.apply_huffman_encoding(self.bitstream, self.huffman_table)

        return self.bitstream

    def find_longest_match(self, data: str, index: int) -> tuple:
        best_match_length = 0
        best_match_offset = 0

        window_start = max(0, index - self.window_size)
        buffer_end = min(len(data), index + self.lookahead_buffer_size)

        for i in range(index - window_start, 0, -1):
            for j in range(index, buffer_end):
                if data[window_start+i-1] != data[j]:
                    break
                elif j - index + 1 > best_match_length:
                    best_match_length = j - index + 1
                    best_match_offset = i - 1

        return (best_match_length, best_match_offset)

    def build_huffman_tree(self, freq_dict):
        heap = [[freq, [char, ""]] for char, freq in freq_dict.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            low_freq_pair = heapq.heappop(heap)
            high_freq_pair = heapq.heappop(heap)
            for pair in low_freq_pair[1:]:
                pair[1] = '0' + pair[1]
            for pair in high_freq_pair[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [low_freq_pair[0] + high_freq_pair[0]] + low_freq_pair[1:] + high_freq_pair[1:])

        huffman_tree = dict(sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p)))
        return huffman_tree

    def apply_huffman_encoding(self, bitstream, huffman_table):
        encoded = ""
        for char in bitstream:
            encoded += huffman_table[char]
        return encoded

    def decode(self, data: str) -> str:
        # Decode the bitstream using the Huffman table
        huffman_dict = dict((v, k) for k, v in self.huffman_table.items())
        bitstream = ""
        output_string = ""
        index = 0
        while index < len(data):
            bitstream += data[index]
            if bitstream in huffman_dict:
                output_string += huffman_dict[bitstream]
                bitstream = ""
            index += 1

        # Decompress the LZ77 encoded data
        decoded_string = ""
        index = 0
        while index < len(output_string):
            if output_string[index] == "0":
                decoded_char = chr(int(output_string[index+1:index+9], 2))
                decoded_string += decoded_char
                index += 9
            else:
                match_length = int(output_string[index+1:index+5], 2)
                match_offset = int(output_string[index+5:index+17], 2)
                decoded_string += decoded_string[-match_offset:][:match_length]
                index += 17

        return decoded_string


# створюємо об'єкт класу LZ77HuffmanEncoder
encoder = LZ77HuffmanEncoder()

# задаємо рядок, який потрібно стиснути
original_data = "abracadabraabracadabra"

# кодуємо рядок за допомогою методу encode
compressed_data = encoder.encode(original_data)


# розпаковуємо стиснутий рядок за допомогою методу decode
uncompressed_data = encoder.decode(compressed_data)
print(original_data)
print(uncompressed_data)
# перевіряємо, що початковий рядок та розпакований рядок співпадають
print(original_data == uncompressed_data)  # True