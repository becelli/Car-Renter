def b2d(binary: str):
    """
    Convert binary to decimal
    """
    binary_num = int(binary, 2)
    aux = []
    for i in range(len(binary)):
        aux.append(binary[i])
    return binary_num


def d2b(decimal: int):
    """
    Convert decimal to binary
    """
    return bin(decimal)[2:]


print(b2d("1000101010"))
print(d2b(1000101010))
