from CircularList import CircularList
from  Piece import Piece
from GridLocation import GridLocation

class Board:

    OUTER_LOOP_INDEXES = [
        (5,2), (4,2), (3,2), (2,2), (1,2), (0,2),
        (2,0), (2,1), (2,2), (2,3), (2,4), (2,5),
        (3,0), (3,1), (3,2), (3,3), (3,4), (3,5),
        (3,5), (3,4), (3,3), (3,2), (3,1), (3,0),
    ]

    INNER_LOOP_INDEXES = [
        (4,0), (4,1), (4,2), (4,3), (4,4), (4,5),
        (5,4), (4,4), (3,4), (2,4), (1,4), (0,4),
        (1,5), (1,4), (1,3), (1,2), (1,1), (1,0),
        (0,1), (1,1), (2,1), (3,1), (4,1), (5,1),
    ]

    def __init__(self):
        self.board = self.build_board_grid() 
        self.inner_loop = CircularList([])
        self.outer_loop = CircularList([]) 

    def build_board_grid(self):
        board = [[GridLocation((x, y)) for x in range(6)] for y in range(6)]

        board = []
        for i in range(6):
            for j in range(6):
                board.append(GridLocation((i, j)))


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
        
        
    