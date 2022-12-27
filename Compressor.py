import codecs
import time
from math import log2, ceil

from Decompressor import shannon_decompress, rle_decompress, lz_decompress

import binary_divison


def nctx_compress(file: bytes, compression: int) -> tuple:
    match compression:
        case 0:
            return file, 0
        case 1:
            return shannon_compress(file)
        case _:
            return file, 0


def count_inclusions(file):
    inclusions = {}
    for i in file:
        # byte = codecs.encode(bytes([i]), 'hex')
        byte = bytes([i])
        # print(bytes([i]))
        try:
            inclusions[byte] += 1
        except KeyError:
            inclusions[byte] = 1
    return inclusions


def shannon_compress(file: bytes) -> (bytes, bytes):
    # tree formation
    inclusions = count_inclusions(file)
    size = len(file)

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
    # print("len byte_codes = " + str(len(byte_codes)))
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
    print(f'source = {len(file)}; new = {len(new_file_bytes)} + {len(header)} + 2 ')
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
        case 1:
            return rle_compress(file)
        case 2:
            return lz_compress(file)
        case _:
            return file


def rle_compress(file: bytes) -> bytes:
    size = len(file)
    if size < 5:
        return file
    inclusions = count_inclusions(file)
    bytes_list = sorted(inclusions.items(), key=lambda item: item[1])
    flag = bytes(bytes_list[0][0])

    new_file_bytes = bytearray() + flag

    count = 1
    curr_symbol = None

    for i in range(size):
        byte = bytes([file[i]])
        if curr_symbol != byte:
            if count >= 4:
                new_file_bytes += flag
                new_file_bytes += count.to_bytes(2, 'big', signed=False)
                new_file_bytes += curr_symbol
            else:
                if curr_symbol == flag:
                    new_file_bytes += flag
                    new_file_bytes += count.to_bytes(2, 'big', signed=False)
                    new_file_bytes += flag
                else:
                    if i != 0:
                        new_file_bytes += curr_symbol * count
            curr_symbol = byte
            count = 1
        else:
            count += 1
    if count >= 4:
        new_file_bytes += flag
        new_file_bytes += count.to_bytes(2, 'big', signed=False)
        new_file_bytes += curr_symbol
    else:
        if curr_symbol == flag:
            new_file_bytes += flag
            new_file_bytes += count.to_bytes(2, 'big', signed=False)
            new_file_bytes += flag
        else:
            new_file_bytes += curr_symbol

    print(f"Original size: {size}\nNew size: {len(new_file_bytes)}")
    return new_file_bytes


def pad_binary_str(bin_str: str, req_length: int) -> str:
    res_str = '0' * (req_length - len(bin_str)) + bin_str
    return res_str


def get_bin_str(num: int, padding: int = 0):
    return pad_binary_str(bin(num)[2:], padding)


def lz_get_link_bytes(offset: int, length: int, print_debug: bool = False):
    max_offset = 1023
    max_length = 63
    if offset > max_offset:
        raise ValueError("Exceeded offset value!")
    if length > max_length:
        raise ValueError("Exceeded length value!")

    if print_debug:
        show_byte = get_bin_str(length - 3, 6) + get_bin_str(offset, 10)
        show_byte = show_byte[:8] + "|" + show_byte[8:]
        print(f"link_bytes for offset {offset} and length {length}\n"
              f"l: {get_bin_str(length - 3, 6)}, s: {get_bin_str(offset, 10)}\n"
              f"whole: {show_byte}")

    a = get_bin_str(length - 3, 6) + get_bin_str(offset - 1, 10)

    b = int(get_bin_str(length - 3, 6) + get_bin_str(offset - 1, 10), 2).to_bytes(2, 'big')

    return int(get_bin_str(length - 3, 6) + get_bin_str(offset - 1, 10), 2).to_bytes(2, 'big')


def lz_flag_list_to_byte(flag_list: list[int]) -> bytes:
    flag_list = list(map(str, flag_list))
    bit_string = ''.join(flag_list)
    return int(bit_string, 2).to_bytes(1, 'big')


def lz_compress(file: bytes) -> bytes:
    size = len(file)
    new_file_bytes = bytearray()
    min_len = 3
    window_size = 1023
    max_len = 63
    window = bytearray()
    front_buffer = bytearray()
    flag_list = [-1] * 8
    flag_counter = 0
    symbols_buffer = bytearray()
    i = 0
    while i < size:
        byte = bytes([file[i]])
        front_buffer += byte
        if i < size - 1:
            last_or_breaking = (front_buffer + bytes([file[i+1]])) not in window
        else:
            last_or_breaking = True
        if front_buffer in window and max_len >= len(front_buffer) >= min_len and last_or_breaking:
            if flag_counter < 8:
                flag_list[flag_counter] = 1
                flag_counter += 1
            else:
                new_file_bytes += lz_flag_list_to_byte(flag_list) + symbols_buffer
                symbols_buffer.clear()
                flag_list = [-1] * 8
                flag_list[0] = 1
                flag_counter = 1
            offset = len(window) - window.rfind(front_buffer)
            length = len(front_buffer)
            symbols_buffer += lz_get_link_bytes(offset, length)
            if len(window) + len(front_buffer) > window_size:
                window = window[len(front_buffer):] + front_buffer
            else:
                window += front_buffer
            front_buffer.clear()
        else:
            if front_buffer not in window:
                for k in range(len(front_buffer)):
                    if flag_counter < 8:
                        flag_list[flag_counter] = 0
                        flag_counter += 1
                    else:
                        new_file_bytes += lz_flag_list_to_byte(flag_list) + symbols_buffer
                        symbols_buffer.clear()
                        flag_list = [-1] * 8
                        flag_list[0] = 0
                        flag_counter = 1
                    symbols_buffer += bytes([front_buffer[k]])

                # symbols_buffer += front_buffer

                if len(window) + len(front_buffer) > window_size:
                    window = window[len(front_buffer):] + front_buffer
                else:
                    window += front_buffer
                front_buffer.clear()
        i += 1

    # Write last chunk to file
    for i in range(8):
        if flag_list[i] < 0:
            flag_list[i] = 0
    new_file_bytes += lz_flag_list_to_byte(flag_list) + symbols_buffer
    # new_file_bytes = len(symbols_buffer).to_bytes(1, 'big') + new_file_bytes

    # Fixing jank of leftover front_buffer
    new_file_bytes += front_buffer
    new_file_bytes = len(front_buffer).to_bytes(1, 'big') + new_file_bytes

    # if size < len(new_file_bytes):
    #     print(f"Compression is useless: old size: {size} < new size: {len(new_file_bytes)}")
    #     return file
    return new_file_bytes


def cypher(file: bytes, compression: int) -> bytes:
    match compression:
        case 0:
            return file
        case _:
            return file


if __name__ == '__main__':
    # # filename = "files/folder1/song.mp3"
    filename = "files/song.mp3"
    # filename = "aboba.txt"
    # filename = "small.txt"
    with open(filename, 'rb') as f:
        newfile = lz_compress(f.read())
    # # print('header:', header)
    # # print('header len:', len(header))
    # # print('unheader:')
    # with open("new_" + filename, 'wb') as f:
    #     f.write(lz_decompress(newfile))
    a = '101'
    # length = 5
    # offset = 12
    # print(get_lz_link_bytes(offset, length))
