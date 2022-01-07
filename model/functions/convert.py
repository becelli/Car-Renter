def b2d(binary: int) -> int:
    """
    Convert binary to decimal
    """
    return int(binary, 2)


def d2b(decimal: int) -> int:
    """
    Convert decimal to binary
    """
    return bin(decimal)[2:]


def d2b_list(decimal: int) -> list:
    """
    Convert decimal to binary
    """
    a = list(bin(decimal)[2:])
    b = []
    for i in a:
        b.append(int(i))
    return b
