class Converter:
    def dec2b_list(self, decimal: int) -> list:
        """
        Convert decimal to binary
        """
        a = list(bin(decimal)[2:])
        b = []
        for i in a:
            b.append(int(i))
        return b

    def b_list2dec(self, binary_list: list) -> int:
        """
        Convert a binary array to a decimal
        """
        a = 0
        for i in binary_list:
            a += i * 2 ** (len(binary_list) - binary_list.index(i) - 1)
        return a
