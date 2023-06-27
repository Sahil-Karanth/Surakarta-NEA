from CircularList import CircularList
from  Piece import Piece

class Board:

    def __init__(self):
        self.outer_loop = CircularList([])
        self.inner_loop = CircularList([])
        self.board = [
            [Piece("B")]
        ]

    