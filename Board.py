from CircularList import CircularList
from GridLocation import GridLocation
from itertools import combinations
from utility_functions import oneD_to_twoD_array

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

        self.__build_board()

        self.num_player1_pieces = 12
        self.num_player2_pieces = 12

    def get_board(self):
        return self.board

    def __get_loop_from_text(self, text):
        if text == "INNER":
            return (self.inner_loop, None)
        elif text == "OUTER":
            return (None, self.outer_loop)
        elif text == "BOTH":
            return (self.inner_loop, self.outer_loop)
        
    def get_piece_count(self, colour):
        if colour == "player1":
            return self.num_player1_pieces
        elif colour == "player2":
            return self.num_player2_pieces

    def __build_board(self):
        # board = [[GridLocation((x, y)) for x in range(6)] for y in range(6)]

        board = []
        outer_loop_lst = []
        inner_loop_lst = []

        for j in range(6):
            for i in range(6):
                location = GridLocation((i, j))
                board.append(location)

                if location.get_cords() in Board.OUTER_LOOP_CORDS:
                    outer_loop_lst.append(location)
                
                elif location.get_cords() in Board.INNER_LOOP_CORDS:
                    inner_loop_lst.append(location)

        self.board = [board[i:i+6] for i in range(0, len(board), 6)]
        self.board = oneD_to_twoD_array(board, 6)
        self.inner_loop = CircularList(inner_loop_lst)
        self.outer_loop = CircularList(outer_loop_lst)

    def __is_valid_coordinate(self, coordinate):
        if coordinate[0] < 0 or coordinate[0] > 5:
            return False
        if coordinate[1] < 0 or coordinate[1] > 5:
            return False
        return True
    
    def __is_valid_cord_pair(self, cord1, cord2):
        if not (self.is_valid_coordinate(cord1) and self.is_valid_coordinate(cord2)):
            return False
        return True
    
    def __is_adjacent(self, initial_pos, final_pos):
        x_diff = abs(initial_pos[0] - final_pos[0])
        y_diff = abs(initial_pos[1] - final_pos[1])

        total_diff = x_diff + y_diff

        if total_diff == 1 or total_diff == 2:
            return True
    
    def __check_normal_legal(self, initial_pos, final_pos, player):
        if not self.is_valid_cord_pair(initial_pos, final_pos):
            return False
        
        starting_location = self.board[initial_pos[0]][initial_pos[1]]

        if starting_location.get_piece().get_colour() != player.get_colour():
            return False

        moving_to_location = self.board[final_pos[0]][final_pos[1]]
        
        if moving_to_location.get_piece() == None and self.is_adjacent(initial_pos, final_pos):
            return True
        
        return False
    
    def __get_piece_indexes_at(self, board_loop, cords):
        starting_indexes = []
        for i in range(board_loop.get_length()):
            item = board_loop.get_next_right()
            if item.get_cords() == cords:
                starting_indexes.append(i)

        return starting_indexes

    def __both_locations_vacant(self, start_location, end_location):
        if start_location.get_piece() == None or end_location.get_piece() == None:
            return False
        return True

    def __both_locations_same_loop(self, start_location, end_location):
        if start_location.get_loop() == end_location.get_loop():
            return True
        return False

    def __check_capture_legal(self, initial_pos, final_pos, player): # try all possible captures
        if not self.is_valid_cord_pair(initial_pos, final_pos):
            return False
        
        if initial_pos.get_piece().get_colour() != player.get_colour():
            return False
        
        if initial_pos.get_piece().get_colour() == final_pos.get_piece().get_colour():
            return False

        start_location = self.board[initial_pos[0]][initial_pos[1]]
        end_location = self.board[final_pos[0]][final_pos[1]]

        if not self.both_locations_vacant(start_location, end_location):
            return False
        
        if not self.both_locations_same_loop(start_location, end_location):
            return False

        board_loop_tuple = self.get_loop_from_text(start_location.get_loop())

        if board_loop_tuple[0] != None:  
            starting_indexes = self.get_piece_indexes_at(board_loop_tuple[0], initial_pos)
            for ind in starting_indexes:
                if self.__can_capture_either_direction(start_location, ind, board_loop_tuple[0]):
                    return True
                
        if board_loop_tuple[1] != None:  
            starting_indexes = self.get_piece_indexes_at(board_loop_tuple[1], initial_pos)
            for ind in starting_indexes:
                if self.can_capture_either_direction(start_location, ind, board_loop_tuple[1]):
                    return True

        return False
    
    def check_move_legal(self, initial_pos, final_pos, player):
        if self.__check_normal_legal(initial_pos, final_pos, player) or self.__check_capture_legal(initial_pos, final_pos, player):
            return True
        return False

    def __loop_pieces_same_colour(self, loc1, loc2):
        if (loc1.get_piece().get_colour() == loc2.get_piece().get_colour()) and (loc1.get_cords() != loc2.get_cords()):
            return False
        return True
    
    def __is_valid_capture(self, start_location, end_location, loop_index_count):
        if (end_location.get_piece().get_colour() != start_location.get_piece().get_colour()) and (loop_index_count > 0):
            return True

    def __is_valid_capture_either_direction(self, start_location, loc_right, loc_left, right_loop_count, left_loop_count):
        if self.is_valid_capture(start_location, loc_right, right_loop_count) or self.is_valid_capture(start_location, loc_left, left_loop_count):
            return True
        return False

    def __check_direction_valid(self, start_location, end_location, loop_index_count):
        if self.loop_pieces_same_colour(start_location, end_location):
            return False
        
        if (loop_index_count == 8) and (start_location.get_cords() == end_location.get_cords()):
            return False
        
        return True

    def __can_capture_either_direction(self, start_location, ind, board_loop):

        if board_loop == None:
            return False

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
            
            if not self.check_direction_valid(start_location, loc_right, right_loop_count):
                right_invalid = True

            if self.check_direction_invalid(start_location, loc_left, left_loop_count):
                left_invalid = True
        
            if right_invalid and left_invalid:
                return False
            
    def __switch_piece_board_position(self, initial_pos, final_pos):

        initial_loc = self.board[initial_pos[0]][initial_pos[1]]
        final_loc = self.board[final_pos[0]][final_pos[1]]

        final_loc.set_piece(self.board[initial_pos[0]][initial_pos[1]].get_piece())
        initial_loc.set_piece(None)

        if initial_loc.get_piece().get_colour() == "B":
            self.num_blue_pieces -= 1

        elif initial_loc.get_piece().get_colour() == "G":
            self.num_green_pieces -= 1
        
    def move_piece(self, initial_pos, final_pos, player):
        if self.__check_normal_legal(initial_pos, final_pos, player):
            self.__switch_piece_board_position(initial_pos, final_pos)
  
    def capture_piece(self, initial_pos, final_pos, player):
        if self.__check_capture_legal(initial_pos, final_pos, player):
            self.switch_piece_board_position(initial_pos, final_pos)

        start_location = self.board[initial_pos[0]][initial_pos[1]]
        end_location = self.board[final_pos[0]][final_pos[1]]
            
        board_loop_tuple = self.get_loop_from_text(start_location.get_loop())

        for i,board_loop in enumerate(board_loop_tuple):
            if board_loop == None:
                continue
            board_loop.replace_item(end_location, start_location)
            if i == 0:
                self.outer_loop = board_loop
            elif i == 1:
                self.inner_loop = board_loop

    def __get_adjacent(cords):

        adjacent_lst = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i == 0) and (j == 0):
                    continue

                adjacent_cord = (abs(cords[0] + i), abs(cords[1] + j))

                if (cords[0] + i) < 0 or (cords[1] + j) > 5 or adjacent_cord in adjacent_lst:
                    continue

                adjacent_lst.append(adjacent_cord)

        return adjacent_lst
    
    def check_has_legal_moves(self, location):
        if location.get_piece() == None:
            return False

        board_pieces = []

        for row in self.board:
            for col in row:
                if self.board[row][col].get_piece() == None:
                    continue
                board_pieces.append(self.board[row][col])

        for piece_pair in combinations(board_pieces, 2):
            if self.check_move_legal(piece_pair[0].get_cords(), piece_pair[1].get_cords()):
                return True

        return False





# TODO (generally for MVP)
    # add constants / constant class (e.g. for cordinates, colours, etc.)
    # add comments and docstrings
    # add terminal UI
    # add main game loop
    # work on player class / implementing player functionality




