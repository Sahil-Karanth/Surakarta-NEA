from LoopedTrack import LoopedTrack
from GridLocation import GridLocation
from MultiClassBoardAttributes import MultiClassBoardAttributes
from utility_functions import oneD_to_twoD_array, shuffle_2D_array, twoD_to_oneD_array
from Piece import Piece
from Move import Move
import random

class Board:

    """Represents the board for the game. The main board is represented by a 2D array of GridLocation objects. The board also contains two LoopedTrack objects
    representing the inner and outer looped tracks of the board."""
    
    NUM_BOARD_LOOPS = 4
    SAVED_GAME_STATE_SEPARATOR = "$"
    SAVED_GAME_STATE_EMPTY_CHAR = "."

    OUTER_TRACK_CORDS = [
        (5,2), (4,2), (3,2), (2,2), (1,2), (0,2),
        (2,0), (2,1), (2,2), (2,3), (2,4), (2,5),
        (0,3), (1,3), (2,3), (3,3), (4,3), (5,3),
        (3,5), (3,4), (3,3), (3,2), (3,1), (3,0),
    ]

    INNER_TRACK_CORDS = [
        (4,0), (4,1), (4,2), (4,3), (4,4), (4,5),
        (5,4), (4,4), (3,4), (2,4), (1,4), (0,4),
        (1,5), (1,4), (1,3), (1,2), (1,1), (1,0),
        (0,1), (1,1), (2,1), (3,1), (4,1), (5,1),
    ]


    def __init__(self, player1, player2, game_state_string=None):

        # data structures for the board
        self.__board = []
        self.__inner_track = LoopedTrack([GridLocation(i) for i in self.INNER_TRACK_CORDS])
        self.__outer_track = LoopedTrack([GridLocation(i) for i in self.OUTER_TRACK_CORDS])

        # populate the board with GridLocation objects
        self.__build_board()
        
        # edit the pieces at certain GridLocation objects to match the game state string
        if game_state_string:
            self.__load_game_state(game_state_string)

        # self.__edit_board_for_testing()

        # player objects are also stored in Board solely for MCTS. All other player related methods are in the Game class
        self.__player_tuple = (player1, player2)


        # maps a text representation of a track to a tuple containing the LoopedTrack objects for the inner and outer tracks
        self.track_text_to_tuple_map = {
            MultiClassBoardAttributes.INNER_TRACK_STRING: (self.__inner_track, None),
            MultiClassBoardAttributes.OUTER_TRACK_STRING: (None, self.__outer_track),
            MultiClassBoardAttributes.BOTH_TRACK_STRING: (self.__inner_track, self.__outer_track),
            None: (None, None)
        }

        # maps a player colour to a player object
        self.__player_colour_map = {
            MultiClassBoardAttributes.player_1_colour: player1,
            MultiClassBoardAttributes.player_2_colour: player2
        }

    def get_board_state(self):
        return self.__board
    
    def __edit_board_for_testing(self):
        for row in self.__board:
            for loc in row:
                loc.set_piece(None)

        outer_lst = [GridLocation(i) for i in self.OUTER_TRACK_CORDS]
        inner_lst = [GridLocation(i) for i in self.INNER_TRACK_CORDS]

        YELLOW_TEST_OUTER_LOOP = [(0,3)]
        GREEN_TEST_OUTER_LOOP = []

        YELLOW_TEST_INNER_LOOP = []
        GREEN_TEST_INNER_LOOP = [(5,1)]

        for i in outer_lst:
            if i.get_cords() in YELLOW_TEST_OUTER_LOOP:
                i.set_piece(Piece(MultiClassBoardAttributes.player_1_colour))
            elif i.get_cords() in GREEN_TEST_OUTER_LOOP:
                i.set_piece(Piece(MultiClassBoardAttributes.player_2_colour))
            else:
                i.set_piece(None)

        for i in inner_lst:
            if i.get_cords() in YELLOW_TEST_INNER_LOOP:
                i.set_piece(Piece(MultiClassBoardAttributes.player_1_colour))
            elif i.get_cords() in GREEN_TEST_INNER_LOOP:
                i.set_piece(Piece(MultiClassBoardAttributes.player_2_colour))
            else:
                i.set_piece(None)


        self.__outer_track = LoopedTrack(outer_lst)
        self.__inner_track = LoopedTrack(inner_lst)

        # self.__board[1][3].set_piece(Piece(MultiClassBoardAttributes.player_1_colour))
        # self.__board[1][5].set_piece(Piece(MultiClassBoardAttributes.player_2_colour))

        # self.__board[4][4].set_piece(Piece("y"))
        # self.__board[2][0].set_piece(Piece("g"))

        # self.__board[0][0].set_piece(Piece(MultiClassBoardAttributes.player_1_colour))
        # self.__board[0][1].set_piece(Piece(MultiClassBoardAttributes.player_1_colour))
        self.__board[0][3].set_piece(Piece(MultiClassBoardAttributes.player_1_colour))
        # # self.__board[0][4].set_piece(Piece(MultiClassBoardAttributes.player_1_colour))
        # self.__board[0][5].set_piece(Piece(MultiClassBoardAttributes.player_1_colour))

        # # self.__board[1][1].set_piece(Piece(MultiClassBoardAttributes.player_1_colour))
        # self.__board[1][2].set_piece(Piece(MultiClassBoardAttributes.player_1_colour))
        # # self.__board[1][3].set_piece(Piece(MultiClassBoardAttributes.player_1_colour))
        # self.__board[1][5].set_piece(Piece(MultiClassBoardAttributes.player_1_colour))

        # # self.__board[2][5].set_piece(Piece(MultiClassBoardAttributes.player_1_colour))
        # self.__board[2][4].set_piece(Piece(MultiClassBoardAttributes.player_2_colour))

        # self.__board[4][0].set_piece(Piece(MultiClassBoardAttributes.player_2_colour))
        # self.__board[4][1].set_piece(Piece(MultiClassBoardAttributes.player_2_colour))
        # # self.__board[4][3].set_piece(Piece(MultiClassBoardAttributes.player_2_colour))
        # # self.__board[4][4].set_piece(Piece(MultiClassBoardAttributes.player_2_colour))
        # self.__board[4][5].set_piece(Piece(MultiClassBoardAttributes.player_2_colour))

        # self.__board[5][0].set_piece(Piece(MultiClassBoardAttributes.player_2_colour))
        self.__board[5][1].set_piece(Piece(MultiClassBoardAttributes.player_2_colour))
        # self.__board[5][3].set_piece(Piece(MultiClassBoardAttributes.player_2_colour))
        # self.__board[5][4].set_piece(Piece(MultiClassBoardAttributes.player_2_colour))

    def __load_game_state(self, game_state_string):

        """Updates the pieces at each GridLocation in the board to match the game state string passed in as an argument"""
        
        # split the game state string into a list of strings representing the pieces at each location
        game_state_lst = game_state_string.split(self.SAVED_GAME_STATE_SEPARATOR)

        # replace character representing an empty location with None
        game_state_lst = [None if i == self.SAVED_GAME_STATE_EMPTY_CHAR else i for i in game_state_lst]

        # convert the list of strings into a 6x6 2D array
        game_state_lst = oneD_to_twoD_array(game_state_lst, MultiClassBoardAttributes.MAX_ROW_INDEX + 1)

        for i in range(MultiClassBoardAttributes.MAX_ROW_INDEX + 1):
            for j in range(MultiClassBoardAttributes.MAX_ROW_INDEX + 1):
                
                # get the string representing the piece at the current location
                curr_piece_str = game_state_lst[i][j]
                curr_cords = (i, j)

                # empty location
                if curr_piece_str == None:
                    self.__board[i][j].set_piece(None)

                # location with a piece
                else:
                    self.__board[i][j].set_piece(Piece(curr_piece_str))

                # update the piece at the corresponding location in the outer track
                if curr_cords in self.OUTER_TRACK_CORDS:
                    self.__outer_track.update_piece(curr_cords, curr_piece_str)

                # update the piece at the corresponding location in the inner track
                elif curr_cords in self.INNER_TRACK_CORDS:
                    self.__inner_track.update_piece(curr_cords, curr_piece_str)

    def __get_common_tracks(self, text_track_1, text_track_2):

        """Returns a tuple in the form in the form (inner_track, outer_track) containing the common 
        tracks between the two text track representations passed in as arguments. If a track is not common,
        the corresponding element in the tuple will be None."""

        # get the LoopedTrack tuples for the inner and outer tracks from the text representations
        track_1_tuple = self.track_text_to_tuple_map[text_track_1]
        track_2_tuple = self.track_text_to_tuple_map[text_track_2]

        common_tracks = []

        for a,b in zip(track_1_tuple, track_2_tuple):
            if a and b:
                common_tracks.append(a)

        return tuple(common_tracks)
    
    def __get_track_from_text(self, text_track):

        """Returns the LoopedTrack tuple corresponding to the text representation of a track passed in as an argument"""

        return self.track_text_to_tuple_map[text_track]

    def __build_board(self):

        """Populates the board with GridLocation objects"""

        board = []

        for i in range(MultiClassBoardAttributes.MAX_ROW_INDEX + 1):
            for j in range(MultiClassBoardAttributes.MAX_ROW_INDEX + 1):
                location = GridLocation((i, j))
                board.append(location)

        # convert the 1D array into a 6x6 2D array
        self.__board = oneD_to_twoD_array(board, MultiClassBoardAttributes.MAX_ROW_INDEX + 1)

    def __is_valid_coordinate(self, coordinate):

        """Returns True if coordinate is a valid coordinate on the board otherwise returns False.
        A valid coordinate is a tuple of the form (x, y) where x and y are integers between 0 and 5 inclusive"""        

        if coordinate[0] < MultiClassBoardAttributes.MIN_ROW_INDEX or coordinate[0] > MultiClassBoardAttributes.MAX_ROW_INDEX:
            return False
        
        if coordinate[1] < MultiClassBoardAttributes.MIN_ROW_INDEX or coordinate[1] > MultiClassBoardAttributes.MAX_ROW_INDEX:
            return False
        
        return True
    
    def __is_valid_cord_pair(self, cord1, cord2):
        
        """Returns True if cord1 and cord2 are valid coordinates on the board otherwise returns False"""

        if not (self.__is_valid_coordinate(cord1) and self.__is_valid_coordinate(cord2)):
            return False
        return True
    
    def __are_locs_adjacent(self, start_loc, end_loc):
        
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

        if start_loc.get_piece_colour() != player.get_piece_colour(): # attempting to move opponent's piece
            return False
        
        # if the end location is adjacent to the start location and is empty, the move is legal
        if self.__are_locs_adjacent(start_loc, end_loc) and end_loc.is_empty():
            return True
        
        return False
    
    def __get_looped_track_loc_indexes(self, looped_track, loc):

        """Returns a list of indexes where loc is found in looped_track. looped_track is a LoopedTrack object which
        is an implementation of a circular list data structure."""

        ind_lst = []
    
        cords = loc.get_cords()

        # start at the beginning of the circular list
        looped_track.set_pointer(0, "right")

        for i in range(looped_track.get_length()):
            
            item = looped_track.get_next_right()

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

        if start_loc.get_piece_colour() != player.get_piece_colour(): # attempting to move opponent's piece
            return False
        
        if start_loc.get_piece_colour() == end_loc.get_piece_colour(): # attempting to capture own piece
            return False

        if self.__either_locations_vacant(start_loc, end_loc): # attempting to capture or capture with an empty location
            return False

        # get the LoopedTrack objects for the inner and outer tracks that both start_loc and end_loc are on
        looped_track_tuple = self.__get_common_tracks(start_loc.get_track(), end_loc.get_track())
        
        for looped_track in looped_track_tuple:

            # indexes where start_loc is found in looped_track
            starting_indexes = self.__get_looped_track_loc_indexes(looped_track, start_loc)

            for ind in starting_indexes:

                # right_move and left_move are Move objects representing the legal captures (or None if no legal capture is found in that direction) that can be made iterating through the looped_track
                right_move, left_move = self.__get_capture_either_direction(start_loc, ind, looped_track)

                # legal capture found by iterating right through the looped_track  
                if right_move and right_move.get_end_cords() == end_loc.get_cords():
                    return True
                
                # legal capture found by iterating left through the looped_track
                elif left_move and left_move.get_end_cords() == end_loc.get_cords():
                    return True
                
        return False
        
    def is_legal_move(self, start_loc, end_loc, player, move_type):

        """Returns True if a move from start_loc to end_loc is legal for the player provided as an argument otherwise returns False.
        This public method is used by the Game class to check if a move is legal."""

        if move_type == MultiClassBoardAttributes.NORMAL_MOVE_TYPE:
            return self.__check_normal_legal(start_loc, end_loc, player)
        
        elif move_type == MultiClassBoardAttributes.CAPTURE_MOVE_TYPE:
            return self.__check_capture_legal(start_loc, end_loc, player)

        return False

    def __loc_pieces_same_colour(self, loc1, loc2):

        """Returns True if the pieces at loc1 and loc2 are the same colour and are not the same location otherwise returns False"""

        if (loc1.get_piece_colour() == loc2.get_piece_colour()) and (loc1.get_cords() != loc2.get_cords()):
            return True
        return False
    
    def __is_valid_capture(self, start_location, end_location, loop_count):

        """Returns True if a capture from start_location to end_location is valid with the assumption that no pieces block the path between the two locations
        and the correct player is attempting to make the capture. Otherwise returns False"""

        if end_location.is_empty():
            return False
        
        # not capturing a piece of the same colour and at least one of the 4 board loops has been traversed
        if (end_location.get_piece_colour() != start_location.get_piece_colour()) and (loop_count > 0):
            return True
        
        return False

    def __check_direction_invalid(self, start_location, end_location, loop_count):

        """Returns False if a capture could still potentially be made in the direction moving to end_location otherwise returns True.
        If the method returns True, the capture legality algorithm should continue iterating in this direction."""

        # one of your own pieces is blocking the path in the current direction of iteration through the LoopedTrack
        if self.__loc_pieces_same_colour(start_location, end_location):
            return True
        
        # a piece has been enountered during iteration through the LoopedTrack and none of the 4 board loops have been traversed
        if loop_count == 0 and not end_location.is_empty():
            return True
        
        # you have returned to the starting location and all of the 4 board loops have been traversed
        if (loop_count == self.NUM_BOARD_LOOPS) and (start_location.get_cords() == end_location.get_cords()):
            return True
        
        return False
    
    def __get_capture_either_direction(self, start_location, ind, looped_track):

        """Returns a Move object if a capture can be made in either direction starting at the piece at ind in looped_track. Otherwise it returns False.
        If a valid capture cannot be made with adjacent locations, further locations are checked until either a valid capture is found or
        the direction being checked is can no longer have a valid capture on it."""

        if looped_track == None:
            return False

        looped_track.set_pointer(ind, "right")
        looped_track.set_pointer(ind, "left")

        # the first two vaalues will be the same (the value at ind) so we can skip them
        looped_track.get_next_right()
        looped_track.get_next_left()

        # a Move object representing a valid capture if one is found iterating right through the LoopedTrack
        right_search = self.__search_direction_for_capture(start_location, looped_track, "right")

        # a Move object representing a valid capture if one is found iterating left through the LoopedTrack        
        left_search = self.__search_direction_for_capture(start_location, looped_track, "left")

        return (right_search, left_search)
    
    def __search_direction_for_capture(self, start_location, looped_track, direction):

        """Returns a move object if a valid capture is found in the direction specified by direction. Otherwise it returns False."""

        invalid = False
        loop_count = 0
        prev_loc = start_location

        while not invalid:
            
            # get the next location in the direction specified by direction
            if direction == "left":
                curr_loc = looped_track.get_next_left()
            elif direction == "right":
                curr_loc = looped_track.get_next_right()
            
            # increment loop_count if a board loop has been traversed to get from prev_loc to curr_loc
            if self.__board_loop_used(prev_loc, curr_loc):
                loop_count += 1
            
            # return a Move object representing the capture if a valid capture is found
            if self.__is_valid_capture(start_location, curr_loc, loop_count):
                return Move(start_location, curr_loc, MultiClassBoardAttributes.CAPTURE_MOVE_TYPE)

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
    
    def __board_loop_used(self, prev_loc, curr_loc):

        """Returns True if a loop has been used to get from prev_loc to curr_loc. Otherwise it returns False"""

        prev_cords = prev_loc.get_cords()
        curr_cords = curr_loc.get_cords()

        # a change in x and y cords between adjacent elements in a LoopedTrack object mean a loop has been used
        if prev_cords[0] != curr_cords[0] and prev_cords[1] != curr_cords[1]:
            return True
        
        return False
        
    def __move_piece_with_undo_arg(self, move_obj, undo=False):

        """Makes the move specified by move_obj. If undo is True, the move is made in reverse."""

        # decrement the piece count of the player that has had a piece captured
        if move_obj.get_move_type() == MultiClassBoardAttributes.CAPTURE_MOVE_TYPE:
            self.__update_piece_counts(move_obj.get_end_colour())


        # update the LoopedTrack objects to reflect the move
        self.__update_tracks_after_move(move_obj)


        # for an undo move, the start and end locations are switched
        if undo:
            self.__switch_piece_positions(move_obj.get_end_loc(), move_obj.get_start_loc())
        
        else:
            self.__switch_piece_positions(move_obj.get_start_loc(), move_obj.get_end_loc())

    def move_piece(self, move_obj):
            
            """Makes the move specified by move_obj. This public method is used by the Game class to make a move.
            This method calls the __move_piece_with_undo_arg method with undo=False because this method is only
            part of the undoing process and undoing is handled by the undo_move method."""
    
            self.__move_piece_with_undo_arg(move_obj, undo=False)

    def __update_tracks_after_move(self, move_obj, undo=False):

        """Updates the inner and outer tracks to reflect the move specified by move_obj. If undo is True, the move is made in reverse."""

        self.__inner_track.switch_piece_positions(move_obj.get_start_loc(), move_obj.get_end_loc())
        self.__outer_track.switch_piece_positions(move_obj.get_start_loc(), move_obj.get_end_loc())

        if move_obj.get_move_type() == MultiClassBoardAttributes.CAPTURE_MOVE_TYPE:
            if undo:
                self.__inner_track.update_piece(move_obj.get_end_cords(), move_obj.get_end_colour())
                self.__outer_track.update_piece(move_obj.get_end_cords(), move_obj.get_end_colour())
            else:
                self.__inner_track.remove_piece(move_obj.get_start_cords())
                self.__outer_track.remove_piece(move_obj.get_start_cords())
    
    def __update_piece_counts(self, end_colour):

        """Decrements the piece count of the player that has had a piece captured"""

        if end_colour == MultiClassBoardAttributes.player_1_colour:
            self.__player_tuple[0].remove_piece()

        elif end_colour == MultiClassBoardAttributes.player_2_colour:
            self.__player_tuple[1].remove_piece()

    def undo_move(self, move_obj):

        """Undoes the move specified by move_obj by making the move in reverse"""

        if move_obj.get_move_type() == MultiClassBoardAttributes.CAPTURE_MOVE_TYPE:
            
            # update the LoopedTrack objects to reflect the undo move
            self.__update_tracks_after_move(move_obj, undo=True)

            # update the board to reflect the undo move
            self.__spawn_piece(move_obj.get_start_colour(), move_obj.get_start_loc())
            self.__spawn_piece(move_obj.get_end_colour(), move_obj.get_end_loc())
        
        elif move_obj.get_move_type() == MultiClassBoardAttributes.NORMAL_MOVE_TYPE:
            self.__move_piece_with_undo_arg(move_obj, undo=True)

    def __spawn_piece(self, colour, loc):

        """spawn a piece on the board at loc with colour specified by colour. Only used by the undo_move method"""

        cords = loc.get_cords()
        piece = Piece(colour)

        self.__board[cords[0]][cords[1]].set_piece(piece)
    
    def __get_loc_legal_moves(self, loc, player):

        """Returns a list of legal moves that can be made from loc"""

        legal_moves = []

        # get normal non-capturing legal moves
        for end_loc in self.__get_adjacent_locations(loc):
            if self.is_legal_move(loc, end_loc, player, MultiClassBoardAttributes.NORMAL_MOVE_TYPE):
                legal_moves.append(Move(loc, end_loc, MultiClassBoardAttributes.NORMAL_MOVE_TYPE))

        # get legal captures
        for row in self.__board:
            for end_loc in row:
                if end_loc.get_piece_colour() != player.get_piece_colour() and self.is_legal_move(loc, end_loc, player, MultiClassBoardAttributes.CAPTURE_MOVE_TYPE):
                    legal_moves.append(Move(loc, end_loc, MultiClassBoardAttributes.CAPTURE_MOVE_TYPE))

        return legal_moves
    
    def get_player_legal_moves(self, player_colour):

        """Returns a list of legal moves that can be made by player"""

        legal_moves = []

        player = self.__player_colour_map[player_colour]

        for row in self.__board:
            for loc in row:

                # append legal moves if the location is occupied by a piece of the player's colour
                if loc.get_piece_colour() == player.get_piece_colour():
                    legal_moves += self.__get_loc_legal_moves(loc, player)

        return legal_moves
    
    def get_single_random_legal_move(self, player_colour):

        """Returns a single, random legal move (Move object) that can be made by the player specified by player_colour"""

        # returns a 6x6 2D array with the elements shuffled (randomised between rows and columns)
        shuffled_board = shuffle_2D_array(self.__board)

        for row in shuffled_board:
            for loc in row:
                if loc.get_piece_colour() == player_colour:
                    loc_legal_moves = self.__get_loc_legal_moves(loc, self.__player_colour_map[player_colour])
                    
                    if len(loc_legal_moves) > 0:
                        move = random.choice(loc_legal_moves)

                        return move

    def get_loc_single_capture(self, start_loc):
        
        """returns a possible capture with the piece at loc"""

        # get the LoopedTrack objects for the inner and outer tracks that start_loc is on
        track_tuple = self.__get_track_from_text(start_loc.get_track())

        for track in track_tuple:
            if track == None:
                continue
            
            # indexes where start_loc is found in track
            starting_indexes = self.__get_looped_track_loc_indexes(track, start_loc)

            for ind in starting_indexes:

                # unlike in the __check_capture_legal method, we're not checking for the legality of a specific capture so we can just return the first capture found
                right_move, left_move = self.__get_capture_either_direction(start_loc, ind, track)
                if right_move:
                    return right_move
                
                elif left_move:
                    return left_move
            
        return None

    def __get_edge_locations(self):

        """Returns a list of 4 GridLocation objects that are on the edge of the board"""

        edge_locs = [
            self.__board[MultiClassBoardAttributes.MIN_ROW_INDEX][MultiClassBoardAttributes.MIN_ROW_INDEX],
            self.__board[MultiClassBoardAttributes.MIN_ROW_INDEX][MultiClassBoardAttributes.MAX_ROW_INDEX],
            self.__board[MultiClassBoardAttributes.MAX_ROW_INDEX][MultiClassBoardAttributes.MIN_ROW_INDEX],
            self.__board[MultiClassBoardAttributes.MAX_ROW_INDEX][MultiClassBoardAttributes.MAX_ROW_INDEX]
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
                return Move(start_loc, end_loc, MultiClassBoardAttributes.NORMAL_MOVE_TYPE)
            
        return None

    def get_random_normal_move(self, player_colour):

        """Returns a random normal move (non-capturing move) that can be made. Used by the Easy AI opponent."""

        return random.choice(self.get_player_legal_moves(player_colour))

    def get_piece_count(self, player_number):
        
        """Returns the number of pieces the player with the number specified by player_number has on the board"""

        return self.__player_tuple[player_number - 1].get_piece_count()

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
                game_state_lst.append(MultiClassBoardAttributes.SAVED_GAME_STATE_EMPTY_CHAR)
            else:
                game_state_lst.append(loc.get_piece_colour())

            game_state_lst.append(self.SAVED_GAME_STATE_SEPARATOR)

        # remove the last separator character
        game_state_lst.pop()

        # convert the list into a string
        game_state_string = "".join(game_state_lst)
        
        return game_state_string

