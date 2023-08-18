from CircularList import CircularList
from GridLocation import GridLocation
from BoardConstants import BoardConstants
from utility_functions import oneD_to_twoD_array
from Piece import Piece

class Board:

    def __init__(self, player1, player2):
        self.__board = []
        self.__inner_loop = CircularList([GridLocation(i) for i in BoardConstants.INNER_LOOP_CORDS])
        self.__outer_loop = CircularList([GridLocation(i) for i in BoardConstants.OUTER_LOOP_CORDS])

        self.__build_board()
        # self.__edit_board_for_testing()

        # self.__num_player1_pieces = BoardConstants.NUM_STARTING_PIECES_EACH
        # self.__num_player2_pieces = BoardConstants.NUM_STARTING_PIECES_EACH

        # # TEST CODE
        # self.__num_player1_pieces = 1
        # self.__num_player2_pieces = 2
        # # END TEST CODE

        self.__player1 = player1
        self.__player2 = player2


    def get_board_state(self):
        return self.__board
    
    def __edit_board_for_testing(self):
        for row in self.__board:
            for loc in row:
                loc.set_piece(None)

        outer_lst = [GridLocation(i) for i in BoardConstants.OUTER_LOOP_CORDS]
        inner_lst = [GridLocation(i) for i in BoardConstants.INNER_LOOP_CORDS]

        YELLOW_TEST_OUTER_LOOP = [(2,4), (2,2)]
        GREEN_TEST_OUTER_LOOP = []

        YELLOW_TEST_INNER_LOOP = [(2,4)]
        GREEN_TEST_INNER_LOOP = [(4,4)]


        for i in outer_lst:
            if i.get_cords() in YELLOW_TEST_OUTER_LOOP:
                i.set_piece(Piece("y"))
            elif i.get_cords() in GREEN_TEST_OUTER_LOOP:
                i.set_piece(Piece("g"))
            else:
                i.set_piece(None)

        for i in inner_lst:
            if i.get_cords() in YELLOW_TEST_INNER_LOOP:
                i.set_piece(Piece("y"))
            elif i.get_cords() in GREEN_TEST_INNER_LOOP:
                i.set_piece(Piece("g"))
            else:
                i.set_piece(None)


        self.__outer_loop = CircularList(outer_lst)
        self.__inner_loop = CircularList(inner_lst)

        self.__board[2][4].set_piece(Piece("y"))
        self.__board[0][0].set_piece(Piece("y"))
        self.__board[4][4].set_piece(Piece("g"))
        self.__board[2][2].set_piece(Piece("g"))


    def __get_common_loops(self, text_loop_1, text_loop_2):

        """Returns a tuple in the form in the form (inner_loop, outer_loop) containing the common 
        loops between the two text loop representations passed in as arguments. If a loop is not common,
        the corresponding element in the tuple will be None."""

        loop_text_to_tuple_map = {
            "INNER": (self.__inner_loop, None),
            "OUTER": (None, self.__outer_loop),
            "BOTH": (self.__inner_loop, self.__outer_loop)
        }

        loop_1_tuple = loop_text_to_tuple_map[text_loop_1]
        loop_2_tuple = loop_text_to_tuple_map[text_loop_2]
        common_loops = []

        for a,b in zip(loop_1_tuple, loop_2_tuple):
            if a and b:
                common_loops.append(a)

        return tuple(common_loops)
        

    def __build_board(self):
        board = []

        for i in range(BoardConstants.MAX_ROW_INDEX + 1):
            for j in range(BoardConstants.MAX_ROW_INDEX + 1):
                location = GridLocation((i, j))
                board.append(location)

        self.__board = oneD_to_twoD_array(board, BoardConstants.MAX_ROW_INDEX + 1)
        

    def __is_valid_coordinate(self, coordinate):
        if coordinate[0] < BoardConstants.MIN_ROW_INDEX or coordinate[0] > BoardConstants.MAX_ROW_INDEX:
            return False
        if coordinate[1] < BoardConstants.MIN_ROW_INDEX or coordinate[1] > BoardConstants.MAX_ROW_INDEX:
            return False
        return True
    
    def __is_valid_cord_pair(self, cord1, cord2):
        if not (self.__is_valid_coordinate(cord1) and self.__is_valid_coordinate(cord2)):
            return False
        return True
    
    def __is_adjacent(self, start_loc, end_loc):

        start_cord = start_loc.get_cords()
        end_cord = end_loc.get_cords()

        x_diff = abs(start_cord[0] - end_cord[0])
        y_diff = abs(start_cord[1] - end_cord[1])

        total_diff = x_diff + y_diff
        
        if total_diff in BoardConstants.ADJACENT_CORD_DIFFS:
            return True
    
    def check_normal_legal(self, start_loc, end_loc, player):
        start_cord = start_loc.get_cords()
        end_cord = end_loc.get_cords()

        if start_loc.is_empty():
            return False

        if not self.__is_valid_cord_pair(start_cord, end_cord):
            return False

        if start_loc.get_colour() != player.get_colour():
            return False

        moving_to_location = self.__board[end_cord[0]][end_cord[1]]
        
        if self.__is_adjacent(start_loc, end_loc) and moving_to_location.is_empty(): # ! potentially change to moving_to_location.get_colour() == None
            return True
        
        return False
    
    def __get_piece_indexes_at(self, board_loop, loc):

        """Returns a list of indexes where loc is found in board_loop. Board_loop is a CircularList"""

        ind_lst = []
    
        cords = loc.get_cords()
    
        board_loop.set_pointer(0, "right")
        board_loop.set_pointer(0, "left")

        for i in range(board_loop.get_length()):
            item = board_loop.get_next_right()
            if item.get_cords() == cords:
                ind_lst.append(i)

        return ind_lst

    def __either_locations_vacant(self, start_location, end_location):

        """Returns True if either start_location or end_location is vacant otherwise returns False"""

        if start_location.is_empty() or end_location.is_empty():
            return True
        return False

    def check_capture_legal(self, start_loc, end_loc, player): # try all possible captures

        start_cords = start_loc.get_cords()
        end_cords = end_loc.get_cords()

        if not self.__is_valid_cord_pair(start_cords, end_cords):
            return False

        if start_loc.get_colour() != player.get_colour():
            return False
        
        if start_loc.get_colour() == end_loc.get_colour():
            return False

        if self.__either_locations_vacant(start_loc, end_loc):
            return False

        board_loop_tuple = self.__get_common_loops(start_loc.get_loop(), end_loc.get_loop())
        
        for board_loop in board_loop_tuple:
            starting_indexes = self.__get_piece_indexes_at(board_loop, start_loc)
            for ind in starting_indexes:
                if self.__can_capture_either_direction(start_loc, ind, board_loop):
                    return True
                
        return False
    

    def is_legal_move(self, start_loc, end_loc, player, move_type):
        if move_type == "move":
            return self.check_normal_legal(start_loc, end_loc, player)
        
        elif move_type == "capture":
            return self.check_capture_legal(start_loc, end_loc, player)

        return False

    def __loop_pieces_same_colour(self, loc1, loc2):
        if (loc1.get_colour() == loc2.get_colour()) and (loc1.get_cords() != loc2.get_cords()):
            return True
        return False
    
    def __is_valid_capture(self, start_location, end_location, loop_count):

        """Returns True if a capture from start_location to end_location is valid otherwise returns False"""

        if end_location.is_empty():
            return False
        if (end_location.get_colour() != start_location.get_colour()) and (loop_count > 0):
            return True
        
        return False


    def __check_direction_valid(self, start_location, end_location, loop_count):

        """Returns True if a capture could still potentially be made in the direction moving to end_location otherwise returns False"""

        if self.__loop_pieces_same_colour(start_location, end_location):
            return False
        
        if loop_count == 0 and not end_location.is_empty():
            return False
        
        if (loop_count == BoardConstants.NUM_BOARD_LOOPS) and (start_location.get_cords() == end_location.get_cords()):
            return False
        
        return True
    

    def __can_capture_either_direction(self, start_location, ind, board_loop):

        """Returns True if a capture can be made in either direction starting at the piece at ind in board_loop. Otherwise it returns False.
        If a valid capture cannot be made with adjacent locations, further locations are checked until either a valid capture is found or
        the direction being checked is can no longer have a valid capture on it."""

        if board_loop == None:
            return False

        board_loop.set_pointer(ind, "right")
        board_loop.set_pointer(ind, "left")

        # the first two will be the same (the value at ind) so we can skip them
        board_loop.get_next_right()
        board_loop.get_next_left()


        if self.__search_direction(start_location, board_loop, "right") or self.__search_direction(start_location, board_loop, "left"):
            return True

        return False
    
    def __search_direction(self, start_location, board_loop, direction):

        """Returns True if a valid capture can be made in the direction specified by direction. Otherwise it returns False."""

        invalid = False
        loop_count = 0
        prev_loc = start_location

        while not invalid:
            
            if direction == "left":
                curr_loc = board_loop.get_next_left()
            elif direction == "right":
                curr_loc = board_loop.get_next_right()
            
            if self.__loop_used(prev_loc, curr_loc):
                loop_count += 1
            
            if self.__is_valid_capture(start_location, curr_loc, loop_count):
                return True
            
            if not self.__check_direction_valid(start_location, curr_loc, loop_count):
                invalid = True

            prev_loc = curr_loc
        
        return False

            
    def __switch_piece_positions(self, start_loc, end_loc):

        """Switches the positions of the pieces at start_loc and end_loc in self.__board"""

        start_cords = start_loc.get_cords()
        end_cords = end_loc.get_cords()

        self.__board[end_cords[0]][end_cords[1]].set_piece(start_loc.get_piece())
        self.__board[start_cords[0]][start_cords[1]].set_piece(None)

    
    def __loop_used(self, prev_loc, curr_loc):

        """Returns True if a loop has been used to get from prev_loc to curr_loc. Otherwise it returns False"""

        prev_cords = prev_loc.get_cords()
        curr_cords = curr_loc.get_cords()

        # a change in x and y cords between adjacent elements in a CircularList board loop mean a loop has been used
        if prev_cords[0] != curr_cords[0] and prev_cords[1] != curr_cords[1]:
            return True
        
        return False

        
    def move_piece(self, start_loc, end_loc, move_type):

        self.__inner_loop.switch_positions(start_loc, end_loc)
        self.__outer_loop.switch_positions(start_loc, end_loc)
        
        if move_type == "capture":
            self.__inner_loop.remove_piece(start_loc)
            self.__outer_loop.remove_piece(start_loc)
            self.__update_piece_counts(end_loc)

        self.__switch_piece_positions(start_loc, end_loc)

    
    def __update_piece_counts(self, end_loc):
        if end_loc.get_colour() == BoardConstants.PLAYER_1_COLOUR:
            self.__player1.remove_piece()

        elif end_loc.get_colour() == BoardConstants.PLAYER_2_COLOUR:
            self.__player2.remove_piece()

