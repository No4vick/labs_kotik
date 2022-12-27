def nctx_decompress(file: bytes, header: bytes, compression: int) -> bytes:
    match compression:
        case 0:
            return file
        case 1:
            return shannon_decompress(file, header)
        case _:
            return file


def shannon_decompress(file: bytes, header: bytes) -> bytes:
    byte_codes, last_byte_len = shannon_deheader(header)
    # print(byte_codes)
    bit_file = file_to_bits(file, last_byte_len)
    # print(bit_file)
    buff = ''
    new_file = bytearray()
    for bit in bit_file:
        buff += bit
        index_res = byte_codes.get(buff)
        if index_res is not None:
            new_file += index_res
            buff = ''
    return new_file


def file_to_bits(file: bytes, last_byte_len: int):
    byte_arr = [''] * len(file)
    for i in range(len(file) - 1):
        byte_arr[i] = bin(file[i])[2:].rjust(8, '0')
        # a = bin(file[i])
        # byte_arr[i] = bin(file[i])[2:]
    # last byte parse
    byte_arr[-1] = bin(file[-1])[2:].rjust(last_byte_len, '0')

    return ''.join(byte_arr)


def shannon_deheader(header: bytes) -> (dict, int):
    last_byte_len = header[0]
    byte_codes = dict()
    for i in range(1, len(header), 4):
        code = bin(int.from_bytes((header[i + 2:i + 3] + header[i + 3:i + 4]), 'big'))[2:]
        if len(code) < header[i]:
            code = code.rjust(header[i], '0')
        # byte_codes[header[i+1:i+2]] = code
        byte_codes[code] = header[i + 1:i + 2]
    return byte_codes, last_byte_len


def ctx_decompress(file: bytes, compression: int) -> bytes:
    match compression:
        case 0:
            return file
        case 1:
            return rle_decompress(file)
        case 2:
            return lz_decompress(file)
        case _:
            return file


def rle_decompress(file: bytes) -> bytes:
    flag = bytes([file[0]])
    new_file_bytes = bytearray()
    size = len(file)
    count = -1
    # repeated_symbol = None
    # Нужно, чтобы пропустить 1 байт при считывании количества повторений, так как число повторений
    # записывается 2-мя байтами
    jank = False
    for i in range(1, size):
        byte = bytes([file[i]])
        if byte == flag and count < 1:
            count = 0
            continue
        if count == 0:
            count = int.from_bytes(bytes(file[i:i + 2]), 'big')
            continue
        if count > 0:
            # Пропуск 1-й итерации
            if not jank:
                jank = True
                continue
            jank = False
            new_file_bytes += byte * count
            count = -1
            continue
        new_file_bytes += byte
        count = -1
    return new_file_bytes


def pad_binary_str(bin_str: str, req_length: int) -> str:
    res_str = '0' * (req_length - len(bin_str)) + bin_str
    return res_str


def lz_flag_list_from_byte(byte: bytes) -> list[int]:
    byte_str = pad_binary_str(bin(int.from_bytes(byte, 'big'))[2:], 8)
    flag_list = list(map(int, byte_str))
    return flag_list


def lz_count_encoded_length(flag_list: list[int]) -> int:
    return sum([x + 1 for x in flag_list])


def lz_deformat_link(read_bytes: bytes) -> tuple:
    combination = pad_binary_str(bin(int.from_bytes(read_bytes, 'big'))[2:], 16)
    # print(combination[:6])
    # print(combination[6:])
    length = int(combination[:6], 2) + 3
    offset = int(combination[6:], 2) + 1
    return offset, length


def lz_decompress(file: bytes) -> bytes:
    last_len = int.from_bytes(file[:1], 'big')
    file = file[1:]
    size = len(file)
    i = 0
    reading_coding = False
    block_count = 0
    flag_list = []
    new_file_bytes = bytearray()
    window = bytearray()
    while i < size - last_len:
        byte = bytes([file[i]])
        if not reading_coding:
            reading_coding = True
            flag_list = lz_flag_list_from_byte(byte)
        else:
            if block_count < len(flag_list):
                if flag_list[block_count] == 0:
                    new_file_bytes += byte
                    window += byte
                    block_count += 1
                elif flag_list[block_count] == 1:
                    offset, length = lz_deformat_link(byte + bytes([file[i + 1]]))
                    offset_from_start = len(window) - offset
                    decoded = window[offset_from_start:offset_from_start + length]
                    new_file_bytes += decoded
                    window += decoded
                    block_count += 1
                    i += 1
            else:
                reading_coding = False
                block_count = 0
                continue
        i += 1
    if last_len > 0:
        new_file_bytes += file[-last_len:]
    return new_file_bytes


def decypher(file: bytes, compression: int) -> bytes:
    match compression:
        case 0:
            return file
        case _:
            return file
