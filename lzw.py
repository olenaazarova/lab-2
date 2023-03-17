from time import time
class LZW:
    """
    this class allows to use LZW algorithm for encoding and decoding
    """
    def __init__(self, message, code_dict={}):
        """
        init method
        message - message that has to be encoded or decoded
        code_dict - start dictionary
        """
        self.message = message
        self.code_dict = code_dict

    def encode(self, message):
        """
        encode the message using lzw algorithm
        """
        self.message = message
        code = 0
        for elem in self.message:
            if elem not in self.code_dict:
                self.code_dict[elem] = code
                code += 1
        encoded_mes = ''
        message = self.message
        j = 0
        cur_symbol = ''
        cod_dict = self.code_dict.copy()
        length = 1
        while j+length < len(message):
            cur_symbol = message[j:j+length]
            next_symbol = message[j+length]
            line = cur_symbol + next_symbol
            length += 1
            if line not in cod_dict:
                cod_dict[line] = code
                code += 1

                encoded_mes += str(cod_dict[cur_symbol])+','
                length = 1
                j += len(line) - 1

        if length == 1:
            encoded_mes += str(cod_dict[message[-1]])
        else:
            if j + length == len(message):
                encoded_mes += str(cod_dict[cur_symbol]) + ',' + str(cod_dict[message[-1]])

        return encoded_mes

    def decode(self, message):
        """
        decode the message using lzw algorithm
        """
        self.message = message
        cod_dict1 = self.code_dict.copy()
        cod_dict2 = cod_dict1.copy()

        cod_dict2 = {v: k for k, v in cod_dict2.items()}

        encoded = self.message.split(',')
        decoded_mes = ''
        i = 0
        index = 0
        code = len(cod_dict1)

        while i < len(encoded):
            if int(encoded[i]) in cod_dict2:
                decoded_mes += cod_dict2[int(encoded[i])]
                i += 1
            else:
                length = 1
                cur_symbol = ''
                flag = False
                while index+length < len(decoded_mes):
                    flag = True
                    cur_symbol = decoded_mes[index:index+length]
                    next_symbol = decoded_mes[index+length]
                    line = cur_symbol + next_symbol
                    length += 1
                    if line not in cod_dict1:
                        cod_dict1[line] = code
                        cod_dict2[code] = line
                        code += 1
                        length = 1
                        index += len(line) - 1

                if int(encoded[i]) not in cod_dict2:
                    if flag:
                        line = decoded_mes[index:]
                        line += line[0]

                    else:
                        line = decoded_mes[-1] + decoded_mes[-1]

                    cod_dict1[line] = code
                    cod_dict2[code] = line
                    code += 1
                    index += len(line) - 1
                    length = 1

        return decoded_mes


if __name__ == "__main__":
    with open('text_example.txt', 'r', encoding='utf-8') as file:
        text = ''.join(file.readlines())

        lzw = LZW(text)
        # measure the compression time
        start = time()
        enc_mes = lzw.encode(text)
        print(f"Time of compress with a file size of {len(text)} characters:  \t\
        {time() - start}s\t= {round((time() - start)/60, 5)}min.(+-)")

        # measure the decompression time
        start = time()
        dec_mes = lzw.decode(enc_mes)

        print(f"Time of decompress with a file size of {len(text)} characters:\t\
        {time() - start}s\t= {round((time() - start)/60, 5)}min.(+-)")

        # print the percentage of file compression

        print(f'Percentage of compression with a file size of {len(text)} characters:\
        \t{len(enc_mes)*(10 + 6 + 8)/len(text.encode())/8*100}%')

        assert dec_mes == text
