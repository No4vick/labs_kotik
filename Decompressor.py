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
     #last byte parse
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
        case _:
            return file


def decypher(file: bytes, compression: int) -> bytes:
    match compression:
        case 0:
            return file
        case _:
            return file
