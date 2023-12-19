from CircularList import CircularList
from GridLocation import GridLocation
from BoardConstants import BoardConstants
from utility_functions import oneD_to_twoD_array, shuffle_2D_array, twoD_to_oneD_array
from Piece import Piece
from Move import Move
import random

class Board:

    def __init__(self, player1, player2, game_state_string=None):
        self.__board = []
        self.__inner_loop = CircularList([GridLocation(i) for i in BoardConstants.INNER_LOOP_CORDS])
        self.__outer_loop = CircularList([GridLocation(i) for i in BoardConstants.OUTER_LOOP_CORDS])
        self.count_test = 0
        self.__game_over = False # used by the MCTS AI opponent

        self.__build_board()

        if game_state_string:
            self.__load_game_state(game_state_string)

        # self.__edit_board_for_testing()

        self.__player_lst = [player1, player2]


        self.loop_text_to_tuple_map = {
            "INNER": (self.__inner_loop, None),
            "OUTER": (None, self.__outer_loop),
            "BOTH": (self.__inner_loop, self.__outer_loop),
            None: (None, None)
        }


        self.__player_colour_map = {
            BoardConstants.player_1_colour: player1,
            BoardConstants.player_2_colour: player2
        }

        # ! MIGRATE THESE TO BOARD CONTSTANTS
        BoardConstants.SAVED_GAME_STATE_SEPARATOR = "$"
        BoardConstants.SAVED_GAME_STATE_EMPTY_CHAR = "."


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
        
        game_state_lst = game_state_string.split(BoardConstants.SAVED_GAME_STATE_SEPARATOR)
        game_state_lst = game_state_lst[1:-1] # remove first and last elements as they are empty
        game_state_lst = [None if i == BoardConstants.SAVED_GAME_STATE_EMPTY_CHAR else i for i in game_state_lst]
        game_state_lst = oneD_to_twoD_array(game_state_lst, BoardConstants.MAX_ROW_INDEX + 1)

        for i in range(BoardConstants.MAX_ROW_INDEX + 1):
            for j in range(BoardConstants.MAX_ROW_INDEX + 1):

                curr_piece_str = game_state_lst[i][j]
                curr_cords = (i, j)

                if curr_piece_str == None:
                    self.__board[i][j].set_piece(None)

                else:
                    self.__board[i][j].set_piece(Piece(curr_piece_str))

                if curr_cords in BoardConstants.OUTER_LOOP_CORDS:
                    self.__outer_loop.update_piece(curr_cords, curr_piece_str)

                elif curr_cords in BoardConstants.INNER_LOOP_CORDS:
                    self.__inner_loop.update_piece(curr_cords, curr_piece_str)


        # ! update player piece counts dependign on the game state string


    def __get_common_loops(self, text_loop_1, text_loop_2):

        """Returns a tuple in the form in the form (inner_loop, outer_loop) containing the common 
        loops between the two text loop representations passed in as arguments. If a loop is not common,
        the corresponding element in the tuple will be None."""


        loop_1_tuple = self.loop_text_to_tuple_map[text_loop_1]
        loop_2_tuple = self.loop_text_to_tuple_map[text_loop_2]
        common_loops = []

        for a,b in zip(loop_1_tuple, loop_2_tuple):
            if a and b:
                common_loops.append(a)

        return tuple(common_loops)
    
    def __get_loop_from_text(self, text_loop):
        return self.loop_text_to_tuple_map[text_loop]
        

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


        # ! MAKE THESE CONSTANTS
        if x_diff == 1 or y_diff == 1:
            return True
        
    
    def get_adjacent(self, loc):

        """Returns a list of the grid loccations on thte board that are adjacent to loc"""

        cords = loc.get_cords()
        adjacent_lst = []
        
        for i in range(-1, 2):
            for j in range(-1, 2):
                
                if (i, j) == (0, 0):
                    continue

                adjacent_cord = (cords[0] + i, cords[1] + j)
                
                if (adjacent_cord[0] >= 0 and adjacent_cord[0] <= 5) and (adjacent_cord[1] >= 0 and adjacent_cord[1] <= 5):
                    adjacent_lst.append(adjacent_cord)

        return [self.__board[i[0]][i[1]] for i in adjacent_lst]

    
    def __check_normal_legal(self, start_loc, end_loc, player):
        start_cord = start_loc.get_cords()
        end_cord = end_loc.get_cords()

        if start_loc.is_empty():
            return False

        if not self.__is_valid_cord_pair(start_cord, end_cord):
            return False

        if start_loc.get_colour() != player.get_colour():
            return False

        moving_to_location = self.__board[end_cord[0]][end_cord[1]]
        
        # ! change to just use end_loc instead of moving_to_location
        # ! also reduce this code significatnly by just having if ... then return true else false
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

    def __check_capture_legal(self, start_loc, end_loc, player): # try all possible captures

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
                right_move, left_move = self.__get_capture_either_direction(start_loc, ind, board_loop)

                if right_move and right_move.get_end_cords() == end_loc.get_cords():
                    return True
                
                elif left_move and left_move.get_end_cords() == end_loc.get_cords():
                    return True
            

                # if move == False:
                #     continue
                # elif move.get_end_cords() == end_loc.get_cords():
                #     return True
                
        return False
        

    def is_legal_move(self, start_loc, end_loc, player, move_type):
        if move_type == "move":
            return self.__check_normal_legal(start_loc, end_loc, player)
        
        elif move_type == "capture":
            return self.__check_capture_legal(start_loc, end_loc, player)

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


    def __check_direction_invalid(self, start_location, end_location, loop_count):

        """Returns False if a capture could still potentially be made in the direction moving to end_location otherwise returns True"""

        if self.__loop_pieces_same_colour(start_location, end_location):
            return True
        
        if loop_count == 0 and not end_location.is_empty():
            return True
        
        if (loop_count == BoardConstants.NUM_BOARD_LOOPS) and (start_location.get_cords() == end_location.get_cords()):
            return True
        
        return False
    

    def __get_capture_either_direction(self, start_location, ind, board_loop):

        """Returns a move object if a capture can be made in either direction starting at the piece at ind in board_loop. Otherwise it returns False.
        If a valid capture cannot be made with adjacent locations, further locations are checked until either a valid capture is found or
        the direction being checked is can no longer have a valid capture on it."""

        if board_loop == None:
            return False

        board_loop.set_pointer(ind, "right")
        board_loop.set_pointer(ind, "left")

        # the first two will be the same (the value at ind) so we can skip them
        board_loop.get_next_right()
        board_loop.get_next_left()

        right_search = self.__search_direction_for_capture(start_location, board_loop, "right")

        # if right_search and right_search.get_end_cords() == end_location.get_cords():
        #     return right_search
        
        left_search = self.__search_direction_for_capture(start_location, board_loop, "left")

        # if left_search and left_search.get_end_cords() == end_location.get_cords():
        #     return left_search

        return (right_search, left_search)
    
    def __search_direction_for_capture(self, start_location, board_loop, direction):

        """Returns a move object if a valid capture can be made in the direction specified by direction. Otherwise it returns False.
        If return_capture is True, the method will return the Move object representing the capture if a valid capture is found.
        This is used by the Easy AI opponent"""

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
                return Move(start_location, curr_loc, "capture")

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

        # a change in x and y cords between adjacent elements in a CircularList board loop mean a loop has been used
        if prev_cords[0] != curr_cords[0] and prev_cords[1] != curr_cords[1]:
            return True
        
        return False

        
    def move_piece(self, move_obj, undo=False):

        if move_obj.get_move_type() == "capture":
            self.__update_piece_counts(move_obj.get_end_colour())


        self.__update_loops_after_move(move_obj)


        if undo:
            self.__switch_piece_positions(move_obj.get_end_loc(), move_obj.get_start_loc())
        
        else:
            self.__switch_piece_positions(move_obj.get_start_loc(), move_obj.get_end_loc())


    def __update_loops_after_move(self, move_obj, undo=False):

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
        if end_colour == BoardConstants.player_1_colour:
            self.__player_lst[0].remove_piece()

        elif end_colour == BoardConstants.player_2_colour:
            self.__player_lst[1].remove_piece()

    def undo_move(self, move_obj):

        """Undo the move specified by move_obj by making the move in reverse"""

        if move_obj.get_move_type() == "capture":
            self.__update_loops_after_move(move_obj, undo=True)
            self.__spawn_piece(move_obj.get_start_colour(), move_obj.get_start_loc())
            self.__spawn_piece(move_obj.get_end_colour(), move_obj.get_end_loc())

            # print("OUTER LOOP AFTER CAPTURE UNDO")
            # for i in self.__outer_loop.get_lst_TEST():
            #     print(i.get_cords(), i.get_colour())
        
        elif move_obj.get_move_type() == "move":
            self.move_piece(move_obj, undo=True)

    def __spawn_piece(self, colour, loc):

        """spawn a piece on the board at loc with colour specified by colour. Only used by the undo_move method"""

        cords = loc.get_cords()
        piece = Piece(colour)

        self.__board[cords[0]][cords[1]].set_piece(piece)


    def check_has_legal_moves(self, location, player):

        """Returns True if the location has a legal move to make otherwise returns False"""

        if location.get_piece() == None:
            return False

        opponent_locs = [] # ! CHANGE NAME as this also includes empty locations

        for row in self.__board:
            for loc in row:
                if loc.get_piece() == None or loc.get_colour() == player.get_colour():
                    continue
                opponent_locs.append(loc)

        for end_loc in opponent_locs:
            if self.is_legal_move(location, end_loc, player, "move") or self.is_legal_move(location, end_loc, player, "capture"):
                return True

        return False
    

    def __get_loc_legal_moves(self, loc, player):

        """Returns a list of legal moves that can be made from loc"""

        legal_moves = []

        for end_loc in self.get_adjacent(loc):
            if self.is_legal_move(loc, end_loc, player, "move"):
                legal_moves.append(Move(loc, end_loc, "move"))

        
        # for end_loc in self.__board.get_opponent_locs(player):
        #     if self.is_legal_move(loc, end_loc, player, "capture"):
        #         legal_moves.append(Move(loc, end_loc, "capture"))


        # ! ITERATE OVER ONLY THE LOOPS THAT IT SITS ON

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
                if loc.get_colour() == player.get_colour():
                    legal_moves += self.__get_loc_legal_moves(loc, player)

        return legal_moves
    

    def get_single_legal_move(self, player_colour):

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

        loop_tuple = self.__get_loop_from_text(start_loc.get_loop())

        for loop in loop_tuple:
            if loop == None:
                continue

            starting_indexes = self.__get_piece_indexes_at(loop, start_loc)

            for ind in starting_indexes:
                right_move, left_move = self.__get_capture_either_direction(start_loc, ind, loop)
                if right_move:
                    return right_move
                
                elif left_move:
                    return left_move
            
        return None
    

    def __get_edge_locations(self):

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

        for end_loc in self.get_adjacent(start_loc):
            if end_loc.is_empty():

                return Move(start_loc, end_loc, "move")
            
        return None

    def get_random_move(self):

        """Returns a random normal move that can be made on the board for the Easy AI opponent"""

        shuffled_board = shuffle_2D_array(self.__board)

        for row in shuffled_board:
            for loc in row:
                if loc.get_colour() == BoardConstants.player_2_colour:
                    move = self.__get_adjacent_move(loc)
                    if move:
                        return move
 
        return None



    def get_piece_count(self, player_number):
        return self.__player_lst[player_number - 1].get_piece_count()


    def get_game_state_string(self):

        flat_board = twoD_to_oneD_array(self.__board)

        game_state_string = f"{BoardConstants.SAVED_GAME_STATE_SEPARATOR}"

        for loc in flat_board:
            if loc.is_empty():
                game_state_string += BoardConstants.SAVED_GAME_STATE_EMPTY_CHAR
            else:
                game_state_string += loc.get_colour()

            game_state_string += BoardConstants.SAVED_GAME_STATE_SEPARATOR
        

        return game_state_string



