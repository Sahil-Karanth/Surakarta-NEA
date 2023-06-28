from CircularList import CircularList
from  Piece import Piece
from GridLocation import GridLocation

class Board:

    def __init__(self):
        self.outer_loop = CircularList([])
        self.inner_loop = CircularList([])
        self.board = self.build_board_grid()

    def build_board_grid(self):
        board = [[GridLocation((x, y)) for x in range(6)] for y in range(6)]

        return board
    
    def is_valid_coordinate(self, coordinate):
        if coordinate[0] < 0 or coordinate[0] > 5:
            return False
        if coordinate[1] < 0 or coordinate[1] > 5:
            return False
        return True
    
    def is_valid_cord_pair(self, cord1, cord2):
        if not (self.is_valid_coordinate(cord1) and self.is_valid_coordinate(cord2)):
            return False
        return True
    
    def isadjacent(self, initial_pos, final_pos):
        x_diff = abs(initial_pos[0] - final_pos[0])
        y_diff = abs(initial_pos[1] - final_pos[1])

        total_diff = x_diff + y_diff

        if total_diff == 1 or total_diff == 2:
            return True

    def build_inner_loop(self):
        loop = [
            (1, Piece("B")),
            (2, Piece("B")),
            (3, Piece("B")),
            (4, Piece("B")),
            (5, Piece("B")),
            (6, Piece("B")),
            (7, Piece("B")),
            (8, Piece("B")),
            (6, Piece("B")),
            (9, None),
            (10, None),
            (11, Piece("G")),
            (12, Piece("G")),
            (13, Piece("G")),
            (11, Piece("G")),
            (14, Piece("G")),
            (15, Piece("G")),
            (16, Piece("G")),
            (17, Piece("G")),
            (18, Piece("G")),
            (16, Piece("G")),
            (19, None),
            (20, None),
            (3, Piece("B")),

        ]

        return loop
    
    def check_normal_legal(self, initial_pos, final_pos):
        if not self.is_valid_cord_pair(initial_pos, final_pos):
            return False
        
        if self.board[final_pos[0]][final_pos[1]] == None and self.is_adjacent(initial_pos, final_pos):
            return True
        
        return False
    
    def check_capture_legal(self, initial_pos, final_pos):
        if not self.is_valid_cord_pair(initial_pos, final_pos):
            return False
        
        # NOTE NOT FINISHED

    def get_piece_loop(self, pos_id):
        pass
        
        
    