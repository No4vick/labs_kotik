import codecs
import time
from math import log2, ceil

from Decompressor import shannon_decompress

import binary_divison


def nctx_compress(file: bytes, compression: int) -> tuple:
    match compression:
        case 0:
            return file, 0
        case 1:
            return shannon_compress(file)
        case _:
            return file, 0


def shannon_compress(file: bytes) -> (bytes, bytes):
    # tree formation
    inclusions = {}
    size = len(file)
    for i in file:
        # byte = codecs.encode(bytes([i]), 'hex')
        byte = bytes([i])
        # print(bytes([i]))
        try:
            inclusions[byte] += 1
        except KeyError:
            inclusions[byte] = 1
    # print(inclusions)
    freq_sum = {}
    bytes_list = sorted(inclusions.items(), key=lambda item: item[1], reverse=True)
    bytes_list = [x[0] for x in bytes_list]

    for k in range(len(bytes_list)):
        if k == 0:
            freq_sum[bytes_list[k]] = 0
        else:
            prev_sum = freq_sum[bytes_list[k - 1]]
            current_freq = inclusions[bytes_list[k - 1]]
            freq_sum[bytes_list[k]] = prev_sum + current_freq
    # print(freq_sum)
    byte_codes = {}

    for k in range(len(bytes_list)):
        freq = freq_sum[bytes_list[k]]
        precision = ceil(-log2(inclusions[bytes_list[k]] / size))
        byte_codes[bytes_list[k]] = binary_divison.divide(freq, size, precision)[1]
    # print(byte_codes)
    print("len byte_codes = " + str(len(byte_codes)))
    # file encoding
    new_file_string_arr = [''] * size
    total = 0

    for i in range(size):
        # byte = codecs.encode(bytes([file[i]]), 'hex')
        byte = bytes([file[i]])
        # print(byte_codes[byte])
        # new_file_string += byte_codes[byte]
        new_file_string_arr[i] = byte_codes[byte]
    # print(byte_codes)
    new_file_string = ''.join(new_file_string_arr)
    # print(new_file_string)

    new_file_bytes = bytearray()
    last_byte_len = 0
    for x in range(0, len(new_file_string), 8):
        byte = new_file_string[x:x + 8]
        last_byte_len = len(byte)
        byte = int(byte, 2).to_bytes(1, 'big')
        new_file_bytes += byte
    # print(bytes(new_file_bytes))
    # print(file)
    header = last_byte_len.to_bytes(1, 'big')
    header += shannon_header(byte_codes)

    # print(f'source = {len(file)}; new = {ceil(len(new_file_string) / 8)}')
    return new_file_bytes, header


def shannon_header(byte_codes: dict) -> bytes:
    # print(byte_codes)
    header = bytes()
    for b, c in byte_codes.items():
        # print(b, ':', c, '|', int(c, 2).to_bytes(1, 'big'), bytes(b), bytes(c, encoding='ascii'))
        header += len(c).to_bytes(1, 'big')
        header += b
        try:
            header += int(c, 2).to_bytes(2, 'big')
        except OverflowError:
            print(f'SASNULO: {c}')
    # print(header)
    return header


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
        newfile, header = shannon_compress(f.read())
    # print('header:', header)
    # print('header len:', len(header))
    # print('unheader:')
    with open("new_" + filename, 'wb') as f:
        f.write(shannon_decompress(newfile, header))

