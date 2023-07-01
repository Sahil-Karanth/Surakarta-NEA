from CircularList import CircularList
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

    def get_loop_from_text(self, text):
        if text == "INNER":
            return self.inner_loop
        elif text == "OUTER":
            return self.outer_loop
        else:
            return None

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
    
    def get_piece_indexes_at(self, board_loop, cords):
        starting_indexes = []
        for i in range(board_loop.get_length()):
            item = board_loop.get_next_right()
            if item.get_cords() == cords:
                starting_indexes.append(i)

        return starting_indexes

    def both_locations_vacant(self, start_location, end_location):
        if start_location.get_piece() == None or end_location.get_piece() == None:
            return False
        return True

    def both_locations_same_loop(self, start_location, end_location):
        if start_location.get_loop() == end_location.get_loop():
            return True
        return False

    def check_capture_legal(self, initial_pos, final_pos): # try all possible captures
        if not self.is_valid_cord_pair(initial_pos, final_pos):
            return False

        start_location = self.board[initial_pos[0]][initial_pos[1]]
        end_location = self.board[final_pos[0]][final_pos[1]]

        if not self.both_locations_vacant(start_location, end_location):
            return False
        
        if not self.both_locations_same_loop(start_location, end_location):
            return False

        board_loop = self.get_loop_from_text(start_location.get_loop())

        starting_indexes = self.get_piece_indexes_at(board_loop, initial_pos)

        for ind in starting_indexes:
            if self.can_capture_either_direction(start_location, ind, board_loop):
                return True        
        return False
    
    def loop_pieces_same_colour(self, loc1, loc2):
        if (loc1.get_piece().get_colour() == loc2.get_piece().get_colour()) and (loc1.get_cords() != loc2.get_cords()):
            return False
        return True
    
    def is_valid_capture(self, start_location, end_location, loop_index_count):
        if (end_location.get_piece().get_colour() != start_location.get_piece().get_colour()) and (loop_index_count > 0):
            return True

    def is_valid_capture_either_direction(self, start_location, loc_right, loc_left, right_loop_count, left_loop_count):
        if self.is_valid_capture(start_location, loc_right, right_loop_count) or self.is_valid_capture(start_location, loc_left, left_loop_count):
            return True
        return False

    def check_direction_valid(self, start_location, end_location, loop_index_count):
        if self.loop_pieces_same_colour(start_location, end_location):
            return False
        
        if (loop_index_count == 8) and (start_location.get_cords() == end_location.get_cords()):
            return False
        
        return True

    def can_capture_either_direction(self, start_location, ind, board_loop):
        board_loop.set_current_index(ind)
        left_loop_count = 0
        right_loop_count = 0
        right_invalid = False 
        left_invalid = False
        while True:
            loc_right = board_loop.get_next_right()
            loc_left = board_loop.get_next_left()

            if loc_right.is_loop_index():
                right_loop_count += 1
            
            if loc_left.is_loop_index():
                left_loop_count += 1

            if self.is_valid_capture_either_direction(start_location, loc_right, loc_left, right_loop_count, left_loop_count):
                return True
            
                 # ? call function make the capture?

            if not self.check_direction_valid(start_location, loc_right, right_loop_count):
                right_invalid = True

            if self.check_direction_invalid(start_location, loc_left, left_loop_count):
                left_invalid = True
        
            if right_invalid and left_invalid:
                return False
            












# OLD VERSION OF CAN_CAPTURE_EITHER_DIRECTION

"""
    def can_capture_either_direction(self, start_location, ind):
        self.inner_loop.set_current_index(ind)
        left_loop_count = 0
        right_loop_count = 0

        while True:
            loc_right = self.inner_loop.get_next_right()
            loc_left = self.inner_loop.get_next_left()

            if loc_right.is_loop_index():
                right_loop_count += 1
            
            if loc_left.is_loop_index():
                left_loop_count += 1

            piece_right = loc_right.get_piece()
            piece_left = loc_left.get_piece()

            if self.loop_pieces_same_colour(start_location, piece_right):
                return False

            if self.loop_pieces_same_colour(start_location, piece_left):
                return False
            
            if (piece_right.get_colour() != start_location.get_piece().get_colour()) and right_loop_count > 0:
                return True
            
            if (piece_left.get_colour() != start_location.get_piece().get_colour()) and left_loop_count > 0:
                return True
            
            if (right_loop_count == 8) and (start_location.get_cords() == loc_right.get_cords()):
                return False
            
            if (left_loop_count == 8) and (start_location.get_cords() == loc_left.get_cords()):
                return False
"""