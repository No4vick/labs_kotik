import codecs
from math import log2, ceil

import binary_divison


def nctx_compress(file: bytes, compression: int) -> bytes:
    match compression:
        case 0:
            return file
        case 1:
            return shannon_compress(file)
        case _:
            return file


def shannon_compress(file: bytes) -> bytes:
    # tree formation
    inclusions = {}
    size = len(file)
    for i in file:
        byte = codecs.encode(bytes([i]), 'hex')
        try:
            inclusions[byte] += 1
        except KeyError:
            inclusions[byte] = 1
    print(inclusions)
    freq_sum = {}
    bytes_list = sorted(inclusions.items(), key=lambda item: item[1], reverse=True)
    bytes_list = [x[0] for x in bytes_list]
    print(bytes_list)
    for k in range(len(bytes_list)):
        if k == 0:
            freq_sum[bytes_list[k]] = 0
        else:
            prev_sum = freq_sum[bytes_list[k - 1]]
            current_freq = inclusions[bytes_list[k - 1]]
            freq_sum[bytes_list[k]] = prev_sum + current_freq
    print(freq_sum)
    byte_codes = {}
    for k in range(len(bytes_list)):
        freq = freq_sum[bytes_list[k]]
        precision = ceil(-log2(inclusions[bytes_list[k]] / size))
        byte_codes[bytes_list[k]] = binary_divison.divide(freq, size, precision)[1]
    # file encoding
    file = bytearray(file)
    # for byte in file:
    #     byte = codecs.encode(bytes([byte]), 'hex')
    #     print(byte_codes[byte])
    print(byte_codes)
    return file


def ctx_compress(file: bytes, compression: int) -> bytes:
    match compression:
        case 0:
            return file
        case _:
            return file


def cypher(file: bytes, compression: int) -> bytes:
    match compression:
        case 0:
            return file
        case _:
            return file


if __name__ == '__main__':
    # filename = "files/folder1/song.mp3"
    filename = "kek.txt"
    with open(filename, 'rb') as f:
        shannon_compress(f.read())
