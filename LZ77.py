"""
This module implements the LZ77 algorithm
(Discret project #2)
"""
from time import time
# read file
with open('text0.txt', 'r', encoding="utf-8") as file:
    text = file.read()

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

    def compress(self, string):
        """
        According to the LZ77 compression algorithm, it compresses
        the file and returns a compact encrypted text in the form
        of tuples of the type (offset, length, next_char)
        >>> mini_text = "asdasdasdasdasd"
        >>> print(lzw.compress(mini_text))
        [(0, 0, 'a'), (0, 0, 's'), (0, 0, 'd'), (3, 12, '')]
        """
        data, output, iter = string.encode(), [], 0
        while iter < len(data):
            best_match = (0, 0)
            search_start = max(0, iter - self.window_size)
            for j in range(search_start, iter):
                length = 0
                while iter + length < len(data) and data[j + length] == data[iter + length]:
                    length += 1
                    if length > best_match[1]:
                        best_match = (iter - j, length)
            if best_match[1] > 0:
                try:
                    output.append((best_match[0], best_match[1], data[iter + best_match[1]]))
                except IndexError:
                    output.append((best_match[0], best_match[1], 0))
                iter += best_match[1] + 1
            else:
                output.append((0, 0, data[iter]))
                iter += 1
        return output

    def decompress(self, compressed_data):
        """
        The decompress method takes a compressed sequence of data
        as a list of tuples and returns an expanded string. It
        restores the original data using information from the
        tuples obtained from the compress method.
        >>> lzw.compress([(0, 0, 'a'), (0, 0, 's'), (0, 0, 'd'), (3, 12, '')])
        'asdasdasdasdasd'
        """
        output = b""
        for triple in compressed_data:
            if triple[1] > 0:
                start = len(output) - triple[0]
                for i in range(triple[1]):
                    output += bytes([output[start + i]])
            output += bytes([triple[2]])
        if output[-1] == 0:
            return output[:-1].decode()# becouse 0 at end
        else: return output[:].decode()# becouse 0 at end


lz = LZ77()
# measure the compression time
start = time()
compressed = lz.compress(text)
print(f"Time of compress with a file size of {len(text)} characters:  \t\
{time() - start}s\t= {round((time() - start)/60, 5)}min.(+-)")
# measure the decompression time
start = time()
decompressed = lz.decompress(compressed)
print(f"Time of decompress with a file size of {len(text)} characters:\t\
{time() - start}s\t= {round((time() - start)/60, 5)}min.(+-)")
# printt the percentage of file compression
print(f'Percentage of compression with a file size of {len(text)} characters:\
\t{len(compressed)*(10 + 6 + 8)/len(text.encode())/8*100}%')
# print(decompressed)
assert decompressed == text
