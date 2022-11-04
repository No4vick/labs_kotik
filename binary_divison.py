def divide(a, b, precision):
    int_part = int(a / b)
    frac_part = a / b - int_part
    return bin(int_part)[2:], frac_to_bin(frac_part, precision)


def frac_to_bin(frac, precision):
    res = [''] * precision
    for i in range(precision):
        frac = frac * 2
        res[i] = str(int(frac))
        frac = frac - int(frac)
    res = ''.join(res)
    return res


if __name__ == '__main__':
    print(divide(5, 14, 5))
