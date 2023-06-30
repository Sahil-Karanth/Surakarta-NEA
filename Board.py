from CircularList import CircularList
from  Piece import Piece
from GridLocation import GridLocation

class Board:

    OUTER_LOOP_CORDS = [
        (5,2), (4,2), (3,2), (2,2), (1,2), (0,2),
        (2,0), (2,1), (2,2), (2,3), (2,4), (2,5),
        (3,0), (3,1), (3,2), (3,3), (3,4), (3,5),
        (3,5), (3,4), (3,3), (3,2), (3,1), (3,0),
    ]

    INNER_LOOP_CORDS = [
        (4,0), (4,1), (4,2), (4,3), (4,4), (4,5),
        (5,4), (4,4), (3,4), (2,4), (1,4), (0,4),
        (1,5), (1,4), (1,3), (1,2), (1,1), (1,0),
        (0,1), (1,1), (2,1), (3,1), (4,1), (5,1),
    ]

    def __init__(self):
        self.board = []
        self.inner_loop = CircularList([])
        self.outer_loop = CircularList([])

    def build_board(self):
        board = [[GridLocation((x, y)) for x in range(6)] for y in range(6)]

        board = []
        outer_loop_lst = []
        inner_loop_lst = []

        for i in range(6):
            for j in range(6):
                location = GridLocation((i, j))
                board.append(location)

                if location.get_cords() in Board.OUTER_LOOP_CORDS:
                    outer_loop_lst.append(location)
                
                elif location.get_cords() in Board.INNER_LOOP_CORDS:
                    inner_loop_lst.append(location)

        self.board = board
        self.inner_loop = CircularList(inner_loop_lst)
        self.outer_loop = CircularList(outer_loop_lst)
    
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
    
    def is_adjacent(self, initial_pos, final_pos):
        x_diff = abs(initial_pos[0] - final_pos[0])
        y_diff = abs(initial_pos[1] - final_pos[1])

        total_diff = x_diff + y_diff

        if total_diff == 1 or total_diff == 2:
            return True
    
    def check_normal_legal(self, initial_pos, final_pos):
        if not self.is_valid_cord_pair(initial_pos, final_pos):
            return False
        
        moving_to = self.board[final_pos[0]][final_pos[1]]
        
        if moving_to.get_piece() == None and self.is_adjacent(initial_pos, final_pos):
            return True
        
        return False
    
    def check_capture_legal(self, initial_pos, final_pos): # try all possible captures
        if not self.is_valid_cord_pair(initial_pos, final_pos):
            return False

        location1 = self.board[initial_pos[0]][initial_pos[1]]
        location2 = self.board[final_pos[0]][final_pos[1]]

        if location1.get_piece() == None or location2.get_piece() == None:
            return False
        
        if not location1.get_loop() == location2.get_loop():
            return False
        

        starting_indexes = []
        
        if location1.get_loop() == "INNER":
            for i in range(self.inner_loop.get_length()):
                item = self.inner_loop.get_next_right()
                if item.get_cords() == initial_pos:
                    starting_indexes.append(i)
        

        # TODO
        # include an elif for "OUTER" but change this code so order so it won't be duplicated in the elif
        # try going left/right from all of the grid locations in starting_indexes


    