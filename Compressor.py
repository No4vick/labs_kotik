def nctx_compress(file: bytes, compression: int) -> bytes:
    match compression:
        case 0:
            return file
        case 1:
            return shannon_compress(file)
        case _:
            return file


def shannon_compress(file: bytes) -> bytes:
    print("Doing cool compression!")
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
