"""
This module implements the LZ77 algorithm
(Discret project #2)
"""
from time import time
# read file
with open('text.txt', 'r', encoding="utf-8") as file:
    text = file.read()
    # for a in file.readlines():
    #     print(len(a))

class LZ77:
    """
    This class allows you to use the LZ77 algorithmto compress text and decrypt it.
    >>> lz = LZ77()
    """
    def __init__(self, window_size=1024, buffer_size=64):
        """
        Constructor of the class
        The window_size parameter specifies the size of the search window
        and the buffer_size parameter specifies the size of the input view buffer.
        (By default: window_size=1024, buffer_size=64)
        >>> lzw = LZ77(2048, 32)
        """
        self.window_size = window_size
        self.buffer_size = buffer_size

    def compress(self, data):
        """
        According to the LZ77 compression algorithm, it compresses
        the file and returns a compact encrypted text in the form
        of tuples of the type (offset, length, next_char)
        >>> mini_text = "asdasdasdasdasd"
        >>> print(lzw.compress(mini_text))
        [(0, 0, 'a'), (0, 0, 's'), (0, 0, 'd'), (3, 12, '')]
        """
        output = []
        i = 0
        while i < len(data):
            match_found = False
            best_match = (0, 0)
            search_start = max(0, i - self.window_size)
            search_end = i + self.buffer_size
            for j in range(search_start, i):
                length = 0
                while i + length < len(data) and data[j + length] == data[i + length]:
                    length += 1
                    if length > best_match[1]:
                        best_match = (i - j, length)
            if best_match[1] > 0:
                try:
                    output.append((best_match[0], best_match[1], data[i + best_match[1]]))
                except IndexError:
                    output.append((best_match[0], best_match[1], ''))
                i += best_match[1] + 1
            else:
                output.append((0, 0, data[i]))
                i += 1
        return output

    def decompress(self, compressed_data):
        output = ""
        for triple in compressed_data:
            if triple[1] > 0:
                start = len(output) - triple[0]
                for i in range(triple[1]):
                    output += output[start + i]
            output += triple[2]
        return output
    

mini_text = "asdasdasdasdasd"# for doctests
lzw = LZ77()
lzw.compress(mini_text)
compressed = lzw.compress(text)

decompressed = lzw.decompress(compressed)
assert decompressed == text


start = time()
compressed_data=lz.compress(text)
print(f"Time: {time() - start}s")
decompressed_data = lz.decompress(compressed_data)
print(decompressed_data)
