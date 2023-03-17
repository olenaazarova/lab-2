"""
This module implements Huffman algorithm
"""
from time import time
class Huffman:
    """
    this class allows to use Huffman algorithm for encoding and decoding
    """
    def __init__(self, message:str, res_dict={})-> None:
        """
        message - message, that should be encoded or decoded
        res_dict - dictionary with keys for encoding and decoding
        """
        self.message = message
        self.res_dict = res_dict
    def encode(self, message):
        """
        encode the message using Huffman algorithm
        """
        self.message = message
        freq_dict = {}
        length = len(self.message)

        for elem in self.message:
            if elem not in freq_dict:
                freq_dict[elem] = 1
            else:
                freq_dict[elem] += 1

        for elem in freq_dict:
            freq_dict[elem] /= length
            self.res_dict[elem] = ''
        alphabet = sorted(list(freq_dict.items()), key=lambda x:x[1])
        if len(alphabet) == 1:
            self.res_dict[alphabet[0][0]] = '1'
        else:
            while len(alphabet) > 1:
                new_el = alphabet[0][0] + alphabet[1][0]
                new_val = alphabet[0][1] + alphabet[1][1]
                for i in alphabet[0][0]:
                    self.res_dict[i] = '1' + self.res_dict[i]

                for i in alphabet[1][0]:
                    self.res_dict[i] = '0' + self.res_dict[i]

                alphabet = alphabet[2:]
                alphabet.append((new_el, new_val))
                alphabet = sorted(alphabet, key=lambda x: x[1])

        encoded_mes = ''
        for elem in self.message:
            encoded_mes += self.res_dict[elem]
        return encoded_mes


    def decode(self, message):
        """
        decode the message using Huffman algorithm
        """
       # message = self.message
        dictionary = {v: k for k, v in self.res_dict.items()}
        decoded_mes = ''
        i = 1

        while (message != '') and (i <= len(message)):
            if message[:i] in dictionary:
                decoded_mes += dictionary[message[:i]]
                message = message[i:]
                i = 1
            else:
                i += 1
        return decoded_mes

if __name__ == "__main__":
    with open('text_example.txt', 'r', encoding='utf-8') as file:
        text = ''.join(file.readlines())
        huffman = Huffman(text)
        # measure the compression time
        start = time()
        encoded_message = huffman.encode(text)
        print(f"Time of compress with a file size of {len(text)} characters:  \t\
        {time() - start}s\t= {round((time() - start)/60, 5)}min.(+-)")


        # measure the decompression time
        start = time()
        decoded_message = huffman.decode(encoded_message)
        print(f"Time of decompress with a file size of {len(text)} characters:\t\
        {time() - start}s\t= {round((time() - start)/60, 5)}min.(+-)")


        # print the percentage of file compression    
        compr = (1 - (len(encoded_message) / (len(text.encode("utf-8"))*8))) * 100
      #  print (f"compression: {round(compr, 2)}%")
        print(f'Percentage of compression with a file size of {len(text)} characters:\
\t{compr}%')
        assert decoded_message == text
