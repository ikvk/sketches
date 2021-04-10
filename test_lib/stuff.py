def str_to_int(value: str) -> int:
    """really magic"""
    return int(value)


class Magic:
    def __init__(self, val: str):
        """no magic, sorry"""
        self.value = val
        self.wow = 'o_O'

    @property
    def get_int(self):
        return str_to_int(self.value)

    @staticmethod
    def one(self) -> int:
        return 1
