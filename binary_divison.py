def divide(a, b, precision):
    int_part = int(a / b)
    frac_part = a / b - int_part
    return bin(int_part)[2:], frac_to_bin(frac_part, precision)


def frac_to_bin(frac, precision):
    res = [''] * precision
    i = 0
    while i < precision:
        frac = frac * 2
        res[i] = str(int(frac))
        frac = frac - int(frac)
        i += 1
    res = ''.join(res)
    return res
