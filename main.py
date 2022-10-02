import os, codecs
from math import log2


def get_stats(filename: str):
    # Num of bytes
    size = os.path.getsize(filename)
    print(f"size: {size}")

    # Counting inclusions of every byte
    inclusions = {}
    with open(filename, 'rb') as f:
        for i in range(0, size):
            # Reencoding every byte so python doesn't force ascii
            byte = codecs.encode(f.read(1), 'hex')
            try:
                inclusions[byte] += 1
            except KeyError:
                inclusions[byte] = 1

    print("Info about bytes, sorted by value")
    infos = []
    for k in sorted(inclusions):
        info_size = log2(inclusions[k])
        infos.append(info_size)
        print(f"Byte: {k}, N of inclusions: {inclusions[k]}, probability:{inclusions[k] / size: .4f}, amount of info:"
              f"{info_size: .4f}")

    print("\nInfo about bytes, sorted by probability")
    keys = list(inclusions.keys())
    values = list(inclusions.values())
    for v in sorted(values, reverse=True):
        print(f"Byte: {keys[values.index(v)]}, N of inclusions: {v}, probability:{v / size: .4f}, amount of info:"
              f"{log2(v): .4f}")

    length = sum(infos)
    print(f'\nTotal information size:\nBytes: {size}\nBits: {size * 8}')


if __name__ == '__main__':
    get_stats('Erich_Krause.mp3')
