import codecs
import os
from math import log2


def get_stats(filename: str):
    print(filename + ' stats with byte alphabet:')
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
        probability = inclusions[k] / size
        # info_size = log2(inclusions[k])
        info_size = -log2(probability)
        infos.append(info_size)
        print(repr(f"Byte: {k}, N of inclusions: {inclusions[k]}, probability:{probability: .4f}, amount of info:"
              f"{info_size: .4f}"))

    print("\nInfo about bytes, sorted by probability")
    # keys = list(inclusions.keys())
    # values = list(inclusions.values())
    # for v in sorted(values, reverse=True):
    #     print(repr(f"Byte: {keys[values.index(v)]}, N of inclusions: {v}, probability:{v / size: .4f}, amount of info:"
    #           f"{log2(v): .4f}"))
    for k in sorted(inclusions.items(), key=lambda item: item[1], reverse=True):
        probability = int(k[1]) / size
        info_size = -log2(probability)
        print(repr(f"Byte: {k[0]}, N of inclusions: {k[1]}, probability:{probability: .4f}, amount of info:"
                   f"{info_size: .4f}"))

    length = sum(infos)
    print(f'\nTotal information size: \nBytes: {length / 8}\nBits: {length}\n')


def get_stats_unicode(filename: str):
    print(filename + ' stats with unicode alphabet:')
    # Counting inclusions of every symbol
    inclusions = {}
    size = 0
    with open(filename, 'r', encoding='utf-8') as f:
        symbol = f.read(1)
        while symbol:
            size += 1
            try:
                inclusions[symbol] += 1
            except KeyError:
                inclusions[symbol] = 1
            symbol = f.read(1)

    print("Info about symbols, sorted by value")
    infos = []
    for k in sorted(inclusions):
        probability = inclusions[k]/size
        info_size = -log2(probability)
        infos.append(info_size)
        print(repr(f"Symbol: {k}, N of inclusions: {inclusions[k]}, probability:{probability: .4f}, amount of info:"
              f"{info_size: .4f}"))

    print("\nInfo about symbols, sorted by probability")

    for k in sorted(inclusions.items(), key=lambda item: item[1], reverse=True):
        probability = int(k[1])/size
        info_size = -log2(probability)
        print(repr(f"Symbol: {k[0]}, N of inclusions: {k[1]}, probability:{probability: .4f}, amount of info:"
              f"{info_size: .4f}"))

    length = sum(infos)
    print(f'\nTotal information size: \nBytes: {length / 8}\nBits: {length}\n')


if __name__ == '__main__':
    file = 'text.txt'
    get_stats(file)
    get_stats_unicode(file)
