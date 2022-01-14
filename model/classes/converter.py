class Converter:
    def str2b_list(self, string) -> list:
        """
        Convert decimal to binary
        """
        binary_list = []
        for char in string:
            binary_list.append(int(char))
        return binary_list

    def b_list2str(self, binary_list: list) -> str:
        """
        Convert a binary array to a string
        """
        a = ""
        for i in binary_list:
            a += str(i)
        return a
