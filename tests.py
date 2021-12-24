def b2d(binary):
    """
    Convert binary to decimal
    """
    binary_num = int(binary, 2)
    aux = []
    for i in range(len(binary)):
        aux.append(binary[i])
    return binary_num


def d2b(decimal):
    """
    Convert decimal to binary
    """
    return bin(decimal)[2:]
