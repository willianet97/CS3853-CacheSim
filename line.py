class Line:

    """Class representing a line within a processor's main cache."""

    def __init__(self, size):
        self.queue = 0
        self.modified = 0
        self.valid = 0
        self.tag = 0
        self.data = [0] * size