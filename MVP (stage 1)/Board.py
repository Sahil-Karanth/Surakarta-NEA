from CircularList import CircularList
from GridLocation import GridLocation
from utility_functions import oneD_to_twoD_array
from Piece import Piece
from BoardConstants import BoardConstants

class Board:

    def __init__(self):
        self.__board = []

        self.__build_board()
        self.__edit_board_for_testing()

        self.__inner_loop = CircularList([GridLocation(i) for i in BoardConstants.INNER_LOOP_CORDS])
        self.__outer_loop = CircularList([GridLocation(i) for i in BoardConstants.OUTER_LOOP_CORDS])

        # self.__num_player1_pieces = 12
        # self.__num_player2_pieces = 12

        # TEST CODE
        self.__num_player1_pieces = 1
        self.__num_player2_pieces = 1
        # END TEST CODE

    def get_board_state(self):
        return self.__board
    
    def get_inner_loop_testing(self): # ! DELETE ME
        return self.__inner_loop.get_lst_TEST()

    def __edit_board_for_testing(self): # ! DELETE ME
        for row in self.__board:
            for loc in row:
                loc.set_piece(None)

        outer_lst = [GridLocation(i) for i in BoardConstants.OUTER_LOOP_CORDS]
        inner_lst = [GridLocation(i) for i in BoardConstants.INNER_LOOP_CORDS]

        BLUE_TEST_OUTER_LOOP = [(2,4), (1,3)]
        GREEN_TEST_OUTER_LOOP = []

        BLUE_TEST_INNER_LOOP = [(2,4), (1,3)]
        GREEN_TEST_INNER_LOOP = [(1,1), (4,1)]
        
        for i in BoardConstants.OUTER_LOOP_CORDS:
            if i in BLUE_TEST_OUTER_LOOP:
                outer_lst[BoardConstants.OUTER_LOOP_CORDS.index(i)].set_piece(Piece("y"))
            elif i in GREEN_TEST_OUTER_LOOP:
                outer_lst[BoardConstants.OUTER_LOOP_CORDS.index(i)].set_piece(Piece("g"))
            else:
                outer_lst[BoardConstants.OUTER_LOOP_CORDS.index(i)].set_piece(None)

        for i in BoardConstants.INNER_LOOP_CORDS:
            if i in BLUE_TEST_INNER_LOOP:
                inner_lst[BoardConstants.INNER_LOOP_CORDS.index(i)].set_piece(Piece("y"))
            elif i in GREEN_TEST_INNER_LOOP:
                inner_lst[BoardConstants.INNER_LOOP_CORDS.index(i)].set_piece(Piece("g"))
            else:
                inner_lst[BoardConstants.INNER_LOOP_CORDS.index(i)].set_piece(None)

        self.__outer_loop = CircularList(outer_lst)
        self.__inner_loop = CircularList(inner_lst)

        self.__board[2][4].set_piece(Piece("y"))
        self.__board[1][3].set_piece(Piece("y"))
        self.__board[1][1].set_piece(Piece("y"))
        self.__board[4][1].set_piece(Piece("y"))



    def __get_loop_from_text(self, text):

        """Returns the inner loop, outer loop, or both loops depending on the text passed in.
        A tuple is returned in the form (inner_loop, outer_loop). The loop that is not requested is
        set to None."""

        if text == "INNER":
            return (self.__inner_loop, None)
        elif text == "OUTER":
            return (None, self.__outer_loop)
        elif text == "BOTH":
            return (self.__inner_loop, self.__outer_loop)
        
    def get_piece_count(self, colour):
        if colour == "player1":
            return self.__num_player1_pieces
        elif colour == "player2":
            return self.__num_player2_pieces

    def __build_board(self):

        """Builds the 2D array board in its inital state at the start of the game."""

        board = []
        for i in range(BoardConstants.MAX_ROW_INDEX + 1):
            for j in range(BoardConstants.MAX_ROW_INDEX + 1):
                location = GridLocation((i, j))
                board.append(location)

        self.__board = [board[i:i+6] for i in range(0, len(board), 6)]
        self.__board = oneD_to_twoD_array(board, BoardConstants.MAX_ROW_INDEX + 1)


    def __is_valid_coordinate(self, coordinate):

        """Checks if a coordinate is valid (i.e. between 0 and 5 inclusive)."""

        for i in coordinate:
            if i < BoardConstants.MIN_ROW_INDEX or i > BoardConstants.MAX_ROW_INDEX:
                return False
        return True

    def __is_valid_cord_pair(self, cord1, cord2):
        if not (self.__is_valid_coordinate(cord1) and self.__is_valid_coordinate(cord2)):
            return False
        return True
    
    def __is_adjacent(self, start_loc, end_loc):

        """Checks if two locations are adjacent to each other including diagonally."""

        start_cord = start_loc.get_cords()
        end_cord = end_loc.get_cords()

        x_diff = abs(start_cord[0] - end_cord[0])
        y_diff = abs(start_cord[1] - end_cord[1])

        total_diff = x_diff + y_diff

        if total_diff == 1 or total_diff == 2:
            return True
        
        return False
    
    def check_normal_legal(self, start_loc, end_loc, player):

        """checks if a normal move is legal (i.e. not a capture but rather a move to an adjacent square)."""

        start_cord = start_loc.get_cords()
        end_cord = end_loc.get_cords()

        if start_loc.get_piece() == None:
            return False

        if not self.__is_valid_cord_pair(start_cord, end_cord):
            return False

        if start_loc.get_colour() != player.get_colour():
            return False
        
        if end_loc.get_piece() == None and self.__is_adjacent(start_loc, end_loc):
            return True
        
        return False
    
    def __get_piece_indexes_at(self, board_loop, loc):

        """Returns a list of indexes of a location a given board loop."""

        starting_indexes = []
        cords = loc.get_cords()

        board_loop.set_pointer(0, "right")
        board_loop.set_pointer(0, "left")

        for i in range(board_loop.get_length()):
            item = board_loop.get_next_right()
            if item.get_cords() == cords:
                starting_indexes.append(i)

        return starting_indexes

    def __either_locations_vacant(self, start_location, end_location):
        if start_location.get_piece() == None or end_location.get_piece() == None:
            return True
        return False

    def __both_locations_same_loop(self, start_location, end_location):
        if start_location.get_loop() == "BOTH" or end_location.get_loop() == "BOTH":
            return True
        if start_location.get_loop() == end_location.get_loop():
            return True
        return False

    def check_capture_legal(self, start_loc, end_loc, player):

        """Checks if a capture move is legal. All possible directions through the loop from
        start_loc to end_loc are checked"""

        start_cords = start_loc.get_cords()
        end_cords = end_loc.get_cords()

        if not self.__is_valid_cord_pair(start_cords, end_cords):
            return False

        if start_loc.get_colour() != player.get_colour():
            return False
        
        if start_loc.get_colour() == end_loc.get_piece().get_colour():
            return False

        if self.__either_locations_vacant(start_loc, end_loc):
            return False
        
        if not self.__both_locations_same_loop(start_loc, end_loc):
            return False

        board_loop_tuple = self.__get_loop_from_text(start_loc.get_loop())

        if board_loop_tuple == None:
            return False
        
        for loop in board_loop_tuple:
            if loop != None and self.__valid_loop_capture(loop, start_loc, end_loc):
                return True
        
        return False
    
    def __valid_loop_capture(self, loop, start_loc, end_loc):

        """Checks if a capture move is legal in a given loop."""

        starting_indexes = self.__get_piece_indexes_at(loop, start_loc)
        for ind in starting_indexes:
            if self.__can_capture_either_direction(start_loc, end_loc, ind, loop):
                return True
        return False

    def is_legal_move(self, start_loc, end_loc, player, move_type):
        if move_type == "move":
            return self.check_normal_legal(start_loc, end_loc, player)
        
        elif move_type == "capture":
            self.check_capture_legal(start_loc, end_loc, player)

        return False

    def __loop_pieces_same_colour(self, loc1, loc2):
        if (loc1.get_colour() == loc2.get_colour()) and (loc1.get_cords() != loc2.get_cords()):
            return True
        return False
    
    def __is_valid_capture(self, start_location, end_location, next_location, loop_index_count):
        if next_location.is_empty() or next_location.get_cords() != end_location.get_cords():
            return False
        if (next_location.get_piece().get_colour() != start_location.get_piece().get_colour()) and (loop_index_count > 0):
            return True

    def __is_valid_capture_left_or_right(self, start_location, end_location, loc_right, loc_left, right_loop_count, left_loop_count):

        """Checks if a capture can be made by moving left or right from a given index in a loop's circular list"""

        if self.__is_valid_capture(start_location, end_location, loc_right, right_loop_count) or self.__is_valid_capture(start_location, end_location, loc_left, left_loop_count):
            return True
        return False

    def __check_direction_valid(self, start_location, end_location, loop_index_count):

        if self.__loop_pieces_same_colour(start_location, end_location):
            return False
        
        if (loop_index_count == 8) and (start_location.get_cords() == end_location.get_cords()):
            return False
        
        return True

    def __can_capture_either_direction(self, start_location, end_loc, ind, board_loop):

        """"checks if a capture can be made by moving left or right from a given index in a loop's circular list"""

        if board_loop == None:
            return False

        board_loop.set_pointer(ind, "right")
        board_loop.set_pointer(ind, "left")

        left_loop_count = 0
        right_loop_count = 0
        right_invalid = False 
        left_invalid = False

        # the first two will be the same (the value at ind) so we can skip them
        board_loop.get_next_right()
        board_loop.get_next_left()

        while True: # ! Ask Mr Gray about how to make this more efficient
            loc_right = board_loop.get_next_right()
            loc_left = board_loop.get_next_left()

            if loc_right.is_loop_index():
                right_loop_count += 1
            
            if loc_left.is_loop_index():
                left_loop_count += 1

            if self.__is_valid_capture_left_or_right(start_location, end_loc, loc_right, loc_left, right_loop_count, left_loop_count):
                return True
            
            if not self.__check_direction_valid(start_location, loc_right, right_loop_count):
                right_invalid = True

            if not self.__check_direction_valid(start_location, loc_left, left_loop_count):
                left_invalid = True
        
            if right_invalid and left_invalid:
                return False
            
    def __displace_piece(self, start_loc, end_loc):

        """moves a piece from start_loc to end_loc"""

        start_cords = start_loc.get_cords()
        end_cords = end_loc.get_cords()

        self.__board[end_cords[0]][end_cords[1]].set_piece(start_loc.get_piece())
        self.__board[start_cords[0]][start_cords[1]].set_piece(None)
        
    def move_piece(self, start_loc, end_loc):
        self.__displace_piece(start_loc, end_loc)
  
    def capture_piece(self, start_loc, end_loc):
        if end_loc.get_colour() == "y":
            self.__num_player1_pieces -= 1

        elif end_loc.get_colour() == "g":
            self.__num_player2_pieces -= 1

        self.__displace_piece(start_loc, end_loc)

        board_loop_tuple = self.__get_loop_from_text(start_loc.get_loop())

        for i,board_loop in enumerate(board_loop_tuple):
            if board_loop == None:
                continue
            board_loop.displace_item(end_loc, start_loc)
            if i == 0:
                self.__outer_loop = board_loop
            elif i == 1:
                self.__inner_loop = board_loop

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
    
    def check_loc_legal_moves(self, location, player):

        """Checks if any legal moves can be made from a given location."""

        if location.get_piece() == None:
            return False

        opponent_locs = []

        for row in self.__board:
            for loc in row:
                if loc.get_piece() == None or loc.get_colour() == player.get_colour():
                    continue
                opponent_locs.append(loc)

        for end_loc in opponent_locs:
            if self.check_move_legal(location, end_loc, player, "capture") or self.check_move_legal(location, end_loc, player, "move"):
                return True

        return False