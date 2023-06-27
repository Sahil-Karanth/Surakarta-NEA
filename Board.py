from CircularList import CircularList

class Board:

    def __init__(self):
        self.outer_loop = CircularList([])
        self.inner_loop = CircularList([])
        self.board = []