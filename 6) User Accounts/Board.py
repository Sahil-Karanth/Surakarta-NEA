from CircularList import CircularList
from GridLocation import GridLocation
from BoardConstants import BoardConstants
from utility_functions import oneD_to_twoD_array, shuffle_2D_array, twoD_to_oneD_array
from Piece import Piece
from Move import Move
import random

class Board:

    """Represents the board for the game. The main board is represented by a 2D array of GridLocation objects. The board also contains two CircularList objects
    representing the inner and outer loops of the board."""

    def __init__(self, player1, player2, game_state_string=None):

        # data structures for the board
        self.__board = []
        self.__inner_loop = CircularList([GridLocation(i) for i in BoardConstants.INNER_LOOP_CORDS])
        self.__outer_loop = CircularList([GridLocation(i) for i in BoardConstants.OUTER_LOOP_CORDS])

        # populate the board with GridLocation objects
        self.__build_board()
        
        # edit the pieces at certain GridLocation objects to match the game state string
        if game_state_string:
            self.__load_game_state(game_state_string)

        # self.__edit_board_for_testing()

        self.__player_lst = [player1, player2]


        # maps a text representation of a loop to a tuple containing the BoardLoop objects for the inner and outer loops
        self.loop_text_to_tuple_map = {
            "INNER": (self.__inner_loop, None),
            "OUTER": (None, self.__outer_loop),
            "BOTH": (self.__inner_loop, self.__outer_loop),
            None: (None, None)
        }

        # maps a player colour to a player object
        self.__player_colour_map = {
            BoardConstants.player_1_colour: player1,
            BoardConstants.player_2_colour: player2
        }

    def get_board_state(self):
        return self.__board
    
    def __edit_board_for_testing(self):
        for row in self.__board:
            for loc in row:
                loc.set_piece(None)

        outer_lst = [GridLocation(i) for i in BoardConstants.OUTER_LOOP_CORDS]
        inner_lst = [GridLocation(i) for i in BoardConstants.INNER_LOOP_CORDS]

        YELLOW_TEST_OUTER_LOOP = [(1,2)]
        GREEN_TEST_OUTER_LOOP = [(2,4), (5,3)]

        YELLOW_TEST_INNER_LOOP = [(0,1), (1,2), (1,5)]
        GREEN_TEST_INNER_LOOP = [(2,4), (4,0), (4,1), (4,5), (5,1)]

        for i in outer_lst:
            if i.get_cords() in YELLOW_TEST_OUTER_LOOP:
                i.set_piece(Piece(BoardConstants.player_1_colour))
            elif i.get_cords() in GREEN_TEST_OUTER_LOOP:
                i.set_piece(Piece(BoardConstants.player_2_colour))
            else:
                i.set_piece(None)

        for i in inner_lst:
            if i.get_cords() in YELLOW_TEST_INNER_LOOP:
                i.set_piece(Piece(BoardConstants.player_1_colour))
            elif i.get_cords() in GREEN_TEST_INNER_LOOP:
                i.set_piece(Piece(BoardConstants.player_2_colour))
            else:
                i.set_piece(None)


        self.__outer_loop = CircularList(outer_lst)
        self.__inner_loop = CircularList(inner_lst)

        # self.__board[1][3].set_piece(Piece(BoardConstants.player_1_colour))
        # self.__board[1][5].set_piece(Piece(BoardConstants.player_2_colour))

        # self.__board[4][4].set_piece(Piece("y"))
        # self.__board[2][0].set_piece(Piece("g"))

        self.__board[0][0].set_piece(Piece(BoardConstants.player_1_colour))
        self.__board[0][1].set_piece(Piece(BoardConstants.player_1_colour))
        # self.__board[0][3].set_piece(Piece(BoardConstants.player_1_colour))
        # self.__board[0][4].set_piece(Piece(BoardConstants.player_1_colour))
        self.__board[0][5].set_piece(Piece(BoardConstants.player_1_colour))

        # self.__board[1][1].set_piece(Piece(BoardConstants.player_1_colour))
        self.__board[1][2].set_piece(Piece(BoardConstants.player_1_colour))
        # self.__board[1][3].set_piece(Piece(BoardConstants.player_1_colour))
        self.__board[1][5].set_piece(Piece(BoardConstants.player_1_colour))

        # self.__board[2][5].set_piece(Piece(BoardConstants.player_1_colour))
        self.__board[2][4].set_piece(Piece(BoardConstants.player_2_colour))

        self.__board[4][0].set_piece(Piece(BoardConstants.player_2_colour))
        self.__board[4][1].set_piece(Piece(BoardConstants.player_2_colour))
        # self.__board[4][3].set_piece(Piece(BoardConstants.player_2_colour))
        # self.__board[4][4].set_piece(Piece(BoardConstants.player_2_colour))
        self.__board[4][5].set_piece(Piece(BoardConstants.player_2_colour))

        # self.__board[5][0].set_piece(Piece(BoardConstants.player_2_colour))
        self.__board[5][1].set_piece(Piece(BoardConstants.player_2_colour))
        # self.__board[5][3].set_piece(Piece(BoardConstants.player_2_colour))
        # self.__board[5][4].set_piece(Piece(BoardConstants.player_2_colour))

    def __load_game_state(self, game_state_string):

        """Updates the pieces at each GridLocation in the board to match the game state string passed in as an argument"""
        
        # split the game state string into a list of strings representing the pieces at each location
        game_state_lst = game_state_string.split(BoardConstants.SAVED_GAME_STATE_SEPARATOR)

        # replace character representing an empty location with None
        game_state_lst = [None if i == BoardConstants.SAVED_GAME_STATE_EMPTY_CHAR else i for i in game_state_lst]

        # convert the list of strings into a 6x6 2D array
        game_state_lst = oneD_to_twoD_array(game_state_lst, BoardConstants.MAX_ROW_INDEX + 1)

        for i in range(BoardConstants.MAX_ROW_INDEX + 1):
            for j in range(BoardConstants.MAX_ROW_INDEX + 1):
                
                # get the string representing the piece at the current location
                curr_piece_str = game_state_lst[i][j]
                curr_cords = (i, j)

                # empty location
                if curr_piece_str == None:
                    self.__board[i][j].set_piece(None)

                # location with a piece
                else:
                    self.__board[i][j].set_piece(Piece(curr_piece_str))

                # update the piece at the corresponding location in the outer loop
                if curr_cords in BoardConstants.OUTER_LOOP_CORDS:
                    self.__outer_loop.update_piece(curr_cords, curr_piece_str)

                # update the piece at the corresponding location in the inner loop
                elif curr_cords in BoardConstants.INNER_LOOP_CORDS:
                    self.__inner_loop.update_piece(curr_cords, curr_piece_str)

    def __get_common_loops(self, text_loop_1, text_loop_2):

        """Returns a tuple in the form in the form (inner_loop, outer_loop) containing the common 
        loops between the two text loop representations passed in as arguments. If a loop is not common,
        the corresponding element in the tuple will be None."""

        # get the BoardLoop tuples for the inner and outer loops from the text representations
        loop_1_tuple = self.loop_text_to_tuple_map[text_loop_1]
        loop_2_tuple = self.loop_text_to_tuple_map[text_loop_2]

        common_loops = []

        for a,b in zip(loop_1_tuple, loop_2_tuple):
            if a and b:
                common_loops.append(a)

        return tuple(common_loops)
    
    def __get_loop_from_text(self, text_loop):

        """Returns the BoardLoop tuple corresponding to the text representation of a loop passed in as an argument"""

        return self.loop_text_to_tuple_map[text_loop]

    def __build_board(self):

        """Populates the board with GridLocation objects"""

        board = []

        for i in range(BoardConstants.MAX_ROW_INDEX + 1):
            for j in range(BoardConstants.MAX_ROW_INDEX + 1):
                location = GridLocation((i, j))
                board.append(location)

        # convert the 1D array into a 6x6 2D array
        self.__board = oneD_to_twoD_array(board, BoardConstants.MAX_ROW_INDEX + 1)

    def __is_valid_coordinate(self, coordinate):

        """Returns True if coordinate is a valid coordinate on the board otherwise returns False.
        A valid coordinate is a tuple of the form (x, y) where x and y are integers between 0 and 5 inclusive"""

        if coordinate[0] < BoardConstants.MIN_ROW_INDEX or coordinate[0] > BoardConstants.MAX_ROW_INDEX:
            return False
        
        if coordinate[1] < BoardConstants.MIN_ROW_INDEX or coordinate[1] > BoardConstants.MAX_ROW_INDEX:
            return False
        
        return True
    
    def __is_valid_cord_pair(self, cord1, cord2):
        
        """Returns True if cord1 and cord2 are valid coordinates on the board otherwise returns False"""

        if not (self.__is_valid_coordinate(cord1) and self.__is_valid_coordinate(cord2)):
            return False
        return True
    
    def __is_adjacent(self, start_loc, end_loc):
        
        """Returns True if start_loc and end_loc are adjacent to each other on the board otherwise returns False.
        Diagonal locations are considered adjacent."""

        start_cord = start_loc.get_cords()
        end_cord = end_loc.get_cords()

        x_diff = abs(start_cord[0] - end_cord[0])
        y_diff = abs(start_cord[1] - end_cord[1])


        # if the absolute value of the two x cords and two y cords are different by 1, the locations are adjacent
        if x_diff <= 1 and y_diff <= 1:
            return True
        
    def __get_adjacent_locations(self, loc):

        """Returns a list of the grid locations on the board that are adjacent to the loc GridLocation object passed in as an argument"""

        cords = loc.get_cords()
        adjacent_lst = []
        
        # iterating over the 3x3 grid of locations surrounding the loc GridLocation object
        for i in range(-1, 2):
            for j in range(-1, 2):
                
                # adding (0,0) to the location's coordinates would just give the location itself so we skip it
                if (i, j) == (0, 0):
                    continue

                # the coordinates of the adjacent location by adding the two points together
                adjacent_cord = (cords[0] + i, cords[1] + j)
                
                
                if self.__is_valid_coordinate(adjacent_cord):
                    adjacent_lst.append(adjacent_cord)

        # converting the list of coordinates into a list of GridLocation objects
        return [self.__board[i[0]][i[1]] for i in adjacent_lst]

    def __check_normal_legal(self, start_loc, end_loc, player):

        """Returns True if a normal move from start_loc to end_loc (non-capturing move) is legal for the player provided as an argument otherwise returns False"""

        start_cord = start_loc.get_cords()
        end_cord = end_loc.get_cords()

        # early return conditions
        if start_loc.is_empty():
            return False

        if not self.__is_valid_cord_pair(start_cord, end_cord):
            return False

        if start_loc.get_colour() != player.get_colour(): # attempting to move opponent's piece
            return False
        
        # if the end location is adjacent to the start location and is empty, the move is legal
        if self.__is_adjacent(start_loc, end_loc) and end_loc.is_empty():
            return True
        
        return False
    
    def __get_board_loop_loc_indexes(self, board_loop, loc):

        """Returns a list of indexes where loc is found in board_loop. board_loop is a BoardLoop object which
        is an implementation of a circular list data structure."""

        ind_lst = []
    
        cords = loc.get_cords()

        # start at the beginning of the circular list
        board_loop.set_pointer(0, "right")

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

    def __check_capture_legal(self, start_loc, end_loc, player):

        """Returns True if a capture move from start_loc to end_loc is legal for the player provided as an argument otherwise returns False"""

        start_cords = start_loc.get_cords()
        end_cords = end_loc.get_cords()

        # early return conditions
        if not self.__is_valid_cord_pair(start_cords, end_cords):
            return False

        if start_loc.get_colour() != player.get_colour(): # attempting to move opponent's piece
            return False
        
        if start_loc.get_colour() == end_loc.get_colour(): # attempting to capture own piece
            return False

        if self.__either_locations_vacant(start_loc, end_loc): # attempting to capture or capture with an empty location
            return False

        # get the BoardLoop objects for the inner and outer loops that both start_loc and end_loc are on
        board_loop_tuple = self.__get_common_loops(start_loc.get_loop(), end_loc.get_loop())
        
        for board_loop in board_loop_tuple:

            # indexes where start_loc is found in board_loop
            starting_indexes = self.__get_board_loop_loc_indexes(board_loop, start_loc)

            for ind in starting_indexes:

                # right_move and left_move are Move objects representing the legal captures (or None if no legal capture is found in that direction) that can be made iterating through the board_loop
                right_move, left_move = self.__get_capture_either_direction(start_loc, ind, board_loop)

                # legal capture found by iterating right through the board_loop  
                if right_move and right_move.get_end_cords() == end_loc.get_cords():
                    return True
                
                # legal capture found by iterating left through the board_loop
                elif left_move and left_move.get_end_cords() == end_loc.get_cords():
                    return True
                
        return False
        
    def is_legal_move(self, start_loc, end_loc, player, move_type):

        """Returns True if a move from start_loc to end_loc is legal for the player provided as an argument otherwise returns False.
        This public method is used by the Game class to check if a move is legal."""

        if move_type == "move":
            return self.__check_normal_legal(start_loc, end_loc, player)
        
        elif move_type == "capture":
            return self.__check_capture_legal(start_loc, end_loc, player)

        return False

    def __loc_pieces_same_colour(self, loc1, loc2):

        """Returns True if the pieces at loc1 and loc2 are the same colour and are not the same location otherwise returns False"""

        if (loc1.get_colour() == loc2.get_colour()) and (loc1.get_cords() != loc2.get_cords()):
            return True
        return False
    
    def __is_valid_capture(self, start_location, end_location, loop_count):

        """Returns True if a capture from start_location to end_location is valid with the assumption that no pieces block the path between the two locations
        and the correct player is attempting to make the capture. Otherwise returns False"""

        if end_location.is_empty():
            return False
        
        # not capturing a piece of the same colour and at least one of the board's 4 loops has been traversed
        if (end_location.get_colour() != start_location.get_colour()) and (loop_count > 0):
            return True
        
        return False

    def __check_direction_invalid(self, start_location, end_location, loop_count):

        """Returns False if a capture could still potentially be made in the direction moving to end_location otherwise returns True.
        If the method returns True, the capture legality algorithm should continue iterating in this direction."""

        # one of your own pieces is blocking the path in the current direction of iteration through the board loop
        if self.__loc_pieces_same_colour(start_location, end_location):
            return True
        
        # a piece has been enountered during iteration through the board loop and none of the board's 4 loops have been traversed
        if loop_count == 0 and not end_location.is_empty():
            return True
        
        # you have returned to the starting location and all of the board's 4 loops have been traversed
        if (loop_count == BoardConstants.NUM_BOARD_LOOPS) and (start_location.get_cords() == end_location.get_cords()):
            return True
        
        return False
    
    def __get_capture_either_direction(self, start_location, ind, board_loop):

        """Returns a Move object if a capture can be made in either direction starting at the piece at ind in board_loop. Otherwise it returns False.
        If a valid capture cannot be made with adjacent locations, further locations are checked until either a valid capture is found or
        the direction being checked is can no longer have a valid capture on it."""

        if board_loop == None:
            return False

        board_loop.set_pointer(ind, "right")
        board_loop.set_pointer(ind, "left")

        # the first two vaalues will be the same (the value at ind) so we can skip them
        board_loop.get_next_right()
        board_loop.get_next_left()

        # a Move object representing a valid capture if one is found iterating right through the board loop
        right_search = self.__search_direction_for_capture(start_location, board_loop, "right")

        # a Move object representing a valid capture if one is found iterating left through the board loop        
        left_search = self.__search_direction_for_capture(start_location, board_loop, "left")

        return (right_search, left_search)
    
    def __search_direction_for_capture(self, start_location, board_loop, direction):

        """Returns a move object if a valid capture is found in the direction specified by direction. Otherwise it returns False."""

        invalid = False
        loop_count = 0
        prev_loc = start_location

        while not invalid:
            
            # get the next location in the direction specified by direction
            if direction == "left":
                curr_loc = board_loop.get_next_left()
            elif direction == "right":
                curr_loc = board_loop.get_next_right()
            
            # increment loop_count if a board loop has been traversed to get from prev_loc to curr_loc
            if self.__loop_used(prev_loc, curr_loc):
                loop_count += 1
            
            # return a Move object representing the capture if a valid capture is found
            if self.__is_valid_capture(start_location, curr_loc, loop_count):
                return Move(start_location, curr_loc, "capture")

            # stop iteraating if a blocking condition occurs that means a capture cannot be made in the current direction
            if self.__check_direction_invalid(start_location, curr_loc, loop_count):
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

        # a change in x and y cords between adjacent elements in a BoardLoop object mean a loop has been used
        if prev_cords[0] != curr_cords[0] and prev_cords[1] != curr_cords[1]:
            return True
        
        return False
        
    def move_piece(self, move_obj, undo=False):

        """Moves the piece at start_loc to end_loc. If undo is True, the move is made in reverse."""

        # decrement the piece count of the player that has had a piece captured
        if move_obj.get_move_type() == "capture":
            self.__update_piece_counts(move_obj.get_end_colour())


        # update the board loops to reflect the move
        self.__update_loops_after_move(move_obj)


        # for an undo move, the start and end locations are switched
        if undo:
            self.__switch_piece_positions(move_obj.get_end_loc(), move_obj.get_start_loc())
        
        else:
            self.__switch_piece_positions(move_obj.get_start_loc(), move_obj.get_end_loc())

    def __update_loops_after_move(self, move_obj, undo=False):

        """Updates the inner and outer loops to reflect the move specified by move_obj. If undo is True, the move is made in reverse."""

        self.__inner_loop.switch_positions(move_obj.get_start_loc(), move_obj.get_end_loc())
        self.__outer_loop.switch_positions(move_obj.get_start_loc(), move_obj.get_end_loc())

        if move_obj.get_move_type() == "capture":
            if undo:
                self.__inner_loop.update_piece(move_obj.get_end_cords(), move_obj.get_end_colour())
                self.__outer_loop.update_piece(move_obj.get_end_cords(), move_obj.get_end_colour())
            else:
                self.__inner_loop.remove_piece(move_obj.get_start_cords())
                self.__outer_loop.remove_piece(move_obj.get_start_cords())
    
    def __update_piece_counts(self, end_colour):

        """Decrements the piece count of the player that has had a piece captured"""

        if end_colour == BoardConstants.player_1_colour:
            self.__player_lst[0].remove_piece()

        elif end_colour == BoardConstants.player_2_colour:
            self.__player_lst[1].remove_piece()

    def undo_move(self, move_obj):

        """Undoes the move specified by move_obj by making the move in reverse"""

        if move_obj.get_move_type() == "capture":
            
            # update the board loops to reflect the undo move
            self.__update_loops_after_move(move_obj, undo=True)

            # update the board to reflect the undo move
            self.__spawn_piece(move_obj.get_start_colour(), move_obj.get_start_loc())
            self.__spawn_piece(move_obj.get_end_colour(), move_obj.get_end_loc())
        
        elif move_obj.get_move_type() == "move":
            self.move_piece(move_obj, undo=True)

    def __spawn_piece(self, colour, loc):

        """spawn a piece on the board at loc with colour specified by colour. Only used by the undo_move method"""

        cords = loc.get_cords()
        piece = Piece(colour)

        self.__board[cords[0]][cords[1]].set_piece(piece)

    def check_has_legal_moves(self, location, player):

        """Returns True if the location passed as an argument has a legal move to make otherwise returns False"""

        if location.get_piece() == None:
            return False

        for row in self.__board:
            for end_loc in row:

                # if end_loc has an opponent's piece, check if a legal move can be made to it
                if not end_loc.is_empty() and end_loc.get_colour() != player.get_colour():
                    if self.is_legal_move(location, end_loc, player, "move") or self.is_legal_move(location, end_loc, player, "capture"):
                        return True

        return False
    
    def __get_loc_legal_moves(self, loc, player):

        """Returns a list of legal moves that can be made from loc"""

        legal_moves = []

        # get normal non-capturing legal moves
        for end_loc in self.__get_adjacent_locations(loc):
            if self.is_legal_move(loc, end_loc, player, "move"):
                legal_moves.append(Move(loc, end_loc, "move"))

        # get legal captures
        for row in self.__board:
            for end_loc in row:
                if end_loc.get_colour() != player.get_colour() and self.is_legal_move(loc, end_loc, player, "capture"):
                    legal_moves.append(Move(loc, end_loc, "capture"))

        return legal_moves
    
    def get_legal_moves(self, player_colour):

        """Returns a list of legal moves that can be made by player"""

        legal_moves = []

        player = self.__player_colour_map[player_colour]

        for row in self.__board:
            for loc in row:

                # append legal moves if the location is occupied by a piece of the player's colour
                if loc.get_colour() == player.get_colour():
                    legal_moves += self.__get_loc_legal_moves(loc, player)

        return legal_moves
    
    def get_single_legal_move(self, player_colour):

        """Returns a single, random legal move (Move object) that can be made by the player specified by player_colour"""

        # returns a 6x6 2D array with the elements shuffled (randomised between rows and columns)
        shuffled_board = shuffle_2D_array(self.__board)

        for row in shuffled_board:
            for loc in row:
                if loc.get_colour() == player_colour:
                    loc_legal_moves = self.__get_loc_legal_moves(loc, self.__player_colour_map[player_colour])
                    
                    if len(loc_legal_moves) > 0:
                        move = random.choice(loc_legal_moves)

                        return move

    def get_capture_with(self, start_loc):
        
        """returns a possible capture with the piece at loc"""

        # get the BoardLoop objects for the inner and outer loops that start_loc is on
        loop_tuple = self.__get_loop_from_text(start_loc.get_loop())

        for loop in loop_tuple:
            if loop == None:
                continue
            
            # indexes where start_loc is found in loop
            starting_indexes = self.__get_board_loop_loc_indexes(loop, start_loc)

            for ind in starting_indexes:

                # unlike in the __check_capture_legal method, we're not checking for the legality of a specific capture so we can just return the first capture found
                right_move, left_move = self.__get_capture_either_direction(start_loc, ind, loop)
                if right_move:
                    return right_move
                
                elif left_move:
                    return left_move
            
        return None

    def __get_edge_locations(self):

        """Returns a list of 4 GridLocation objects that are on the edge of the board"""

        edge_locs = [
            self.__board[BoardConstants.MIN_ROW_INDEX][BoardConstants.MIN_ROW_INDEX],
            self.__board[BoardConstants.MIN_ROW_INDEX][BoardConstants.MAX_ROW_INDEX],
            self.__board[BoardConstants.MAX_ROW_INDEX][BoardConstants.MIN_ROW_INDEX],
            self.__board[BoardConstants.MAX_ROW_INDEX][BoardConstants.MAX_ROW_INDEX]
        ]

        return edge_locs

    def get_corner_move(self, start_loc):

        """Returns a move using a corner location to move out of the corner if one is available otherwise returns None"""

        edge_locs = self.__get_edge_locations()

        if start_loc not in edge_locs:
            return None
                
        return self.__get_adjacent_move(start_loc)
            
    def __get_adjacent_move(self, start_loc):

        """Returns a move using a location adjacent to start_loc if one is available otherwise returns None"""

        for end_loc in self.__get_adjacent_locations(start_loc):
            if end_loc.is_empty():
                return Move(start_loc, end_loc, "move")
            
        return None

    def get_random_move(self):

        """Returns a random normal move (non-capturing move) that can be made on the board for the Easy AI opponent"""

        shuffled_board = shuffle_2D_array(self.__board)

        for row in shuffled_board:
            for loc in row:
                
                # if the location is occupied by a piece of the player's colour, return a random adjacent move f one is found
                if loc.get_colour() == BoardConstants.player_2_colour:
                    move = self.__get_adjacent_move(loc)
                    if move:
                        return move
 
        return None

    def get_piece_count(self, player_number):
        
        """Returns the number of pieces the player with the number specified by player_number has on the board"""

        return self.__player_lst[player_number - 1].get_piece_count()

    def get_game_state_string(self):
        
        """Returns a string representation of the current game state. Pieces are represented
        by their colour and empty locations are represented by a pre-determined character. Pieces
        are separated by a pre-determined character. The first and last characters are not
        separator characters."""

        # convert the 2D array into a 1D array
        flat_board = twoD_to_oneD_array(self.__board)

        # list to store game state being saved
        game_state_lst = []

        for loc in flat_board:
            if loc.is_empty():
                game_state_lst.append(BoardConstants.SAVED_GAME_STATE_EMPTY_CHAR)
            else:
                game_state_lst.append(loc.get_colour())

            game_state_lst.append(BoardConstants.SAVED_GAME_STATE_SEPARATOR)

        # remove the last separator character
        game_state_lst.pop()

        # convert the list into a string
        game_state_string = "".join(game_state_lst)
        
        return game_state_string

