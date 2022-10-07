def nctx_decompress(file: bytes, compression: int) -> bytes:
    match compression:
        case 0:
            return file
        case 1:
            return shannon_decompress(file)
        case _:
            return file


def shannon_decompress(file: bytes) -> bytes:
    print("Doing cool decompression!")
    return file


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
