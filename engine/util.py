def convert_color(color):
    if type(color) == str:
        r, g, b = bytes.fromhex(color[-6:])
        return r, g, b


def map_range(value, inmin, inmax, outmin, outmax):
    valueScaled = float(value - inmin) / float(inmax - inmin)
    return outmin + (valueScaled * (outmax - outmin))


def rounded(value, decimals=3):
    return int(value * 10 ** decimals) / 10 ** decimals


def powerlist(array):
    powers = [2 ** i for i in range(len(array) - 1, -1, -1)]

    ret = [rounded(map_range(p, 0, sum(powers), 0, 1)) for p in powers]
    ret[0] += 1.0 - sum(ret)

    return ret


def tileselector(array, size, powers=None):
    from numpy.random import choice

    my_p = powers if powers is not None else powerlist(array)

    return choice(array, size=size, p=my_p)
