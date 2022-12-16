import codecs
import os
from math import log2


def count_n_probabilities(filename, size, n=1):
    inclusions = {}
    with open(filename, 'rb') as f:
        for i in range(0, size, n):
            # NOT reencoding every byte because python is ... I don't know
            # byte = codecs.encode(f.read(symbol_len), 'hex')
            byte = f.read(n)
            try:
                inclusions[byte] += 1
            except KeyError:
                inclusions[byte] = 1

    probs = {}
    # infos = {}
    for curr_byte, byte_count in inclusions.items():
        probs[curr_byte] = byte_count / size
        # infos[curr_byte] = -log2(byte_count / size)
    return probs

def count_inclusions(filename, size):
    inclusions = {}
    with open(filename, 'rb') as f:
        for i in range(0, size, 1):
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
    inclusions = sorted(inclusions.items(), key=lambda item: item[1], reverse=True)
    for k in inclusions:
        probability = int(k[1]) / size
        info_size = -log2(probability)
        print(repr(f"Byte: {k[0]}, N of inclusions: {k[1]}, probability:{probability: .4f}, amount of info:"
                   f"{info_size: .4f}"))

    length = sum(infos)
    print(f'\nTotal information size: \nBytes: {length / 8}\nBits: {length}\n')


def count_inclusions_more_one(filename, size, symbol_len=2):
    inclusions = {}
    with open(filename, 'rb') as f:
        for i in range(0, size, symbol_len):
            # NOT reencoding every byte because python is ... I don't know
            # byte = codecs.encode(f.read(symbol_len), 'hex')
            byte = f.read(symbol_len)
            try:
                inclusions[byte] += 1
            except KeyError:
                inclusions[byte] = 1

    print("Info about bytes, sorted by value")
    infos = []
    single_probs = count_n_probabilities(filename, size, symbol_len - 1)
    for k in sorted(inclusions):
        other_prob = single_probs.get(k[1:])
        probability = (inclusions[k] / size) / other_prob if other_prob is not None else 0
        print(repr(
            f"Byte: {codecs.encode(k, 'hex')}, N of inclusions: {inclusions[k]}, conditional probability:{probability: .4f}"))


def get_stats(filename: str):
    print(filename + ' stats with byte alphabet:')
    # Num of bytes
    size = os.path.getsize(filename)
    print(f"size: {size}")

    # Counting inclusions of every byte
    print("Byte:")
    count_inclusions(filename, size)
    print("2 bytes:")
    count_inclusions_more_one(filename, size, 2)
    print("4 bytes:")
    count_inclusions_more_one(filename, size, 4)

    # get_octets(filename, inclusions, 4)


# def get_stats_unicode(filename: str):
#     print(filename + ' stats with unicode alphabet:')
#     # Counting inclusions of every symbol
#     inclusions = {}
#     size = 0
#     with open(filename, 'r', encoding='utf-8') as f:
#         symbol = f.read(1)
#         while symbol:
#             size += 1
#             try:
#                 inclusions[symbol] += 1
#             except KeyError:
#                 inclusions[symbol] = 1
#             symbol = f.read(1)
#
#     print("Info about symbols, sorted by value")
#     infos = []
#     for k in sorted(inclusions):
#         probability = inclusions[k] / size
#         info_size = -log2(probability)
#         infos.append(info_size)
#         print(repr(f"Symbol: {k}, N of inclusions: {inclusions[k]}, probability:{probability: .4f}, amount of info:"
#                    f"{info_size: .4f}"))
#
#     print("\nInfo about symbols, sorted by probability")
#     inclusions = sorted(inclusions.items(), key=lambda item: item[1], reverse=True)
#     for k in inclusions:
#         probability = int(k[1]) / size
#         info_size = -log2(probability)
#         print(repr(f"Symbol: {k[0]}, N of inclusions: {k[1]}, probability:{probability: .4f}, amount of info:"
#                    f"{info_size: .4f}"))
#
#     length = sum(infos)
#     print(f'\nTotal information size: \nBytes: {length / 8}\nBits: {length}\n')
#
#
# def get_octets(name, byte_list, amount):
#     print('file ' + name + ':')
#     print('the most frequent octets')
#     for k in byte_list[:amount]:
#         print(repr(f"Symbol: {k[0]}, N of inclusions: {k[1]}"))
#
#     print('the most frequent octets that are not codes of printed ascii characters')
#     for k in byte_list:
#         if (int(k[0], 16) > 126) | (int(k[0], 16) < 32):
#             # if int(k[0], 16) < 32:
#             print(repr(f"Symbol: {k[0]}, N of inclusions: {k[1]}"))
#             amount -= 1
#         if amount == 0:
#             break


if __name__ == '__main__':
    file = 'text.txt'
    get_stats(file)
    # get_stats_unicode(file)
