from MultiClassBoardAttributes import MultiClassBoardAttributes
import random
from utility_functions import shuffle_2D_array
from TreeSearch import GameTree

class Player:

    """Represents a player in the game. AI players inherit from this class and human players use this class directly"""

    def __init__(self, name, piece_colour, piece_count=MultiClassBoardAttributes.NUM_STARTING_PIECES_EACH):
        self.__name = name
        self.__piece_colour = piece_colour
        self.__piece_count = piece_count # a player may not have 12 pieces when the object is created if the game is being loaded

    def get_colour(self):
        return self.__piece_colour
    
    def get_name(self):
        return self.__name
    
    def get_piece_count(self):
        return self.__piece_count
    
    def remove_piece(self):
        """Removes a single piece from the player's piece count"""

        if self.__piece_count <= 0:
            raise ValueError("Player has no pieces left, cannot remove piece")
        
        self.__piece_count -= 1
        
    def set_piece_count(self, piece_count):
        self.__piece_count = piece_count
        
    def add_piece(self):

        """Adds a single piece to the player's piece count. Only used to return a piece to a player after a move is undone."""

        if self.__piece_count >= MultiClassBoardAttributes.NUM_STARTING_PIECES_EACH:
            raise ValueError("Player has too many pieces, cannot add piece")
        
        self.__piece_count += 1
    
class AIPlayer(Player):

    """An abstract base class for AI opponents. AI opponent classes inherit from this class and implement the get_move method"""
    
    def __init__(self, name, piece_colour, piece_count=MultiClassBoardAttributes.NUM_STARTING_PIECES_EACH):
        super().__init__(name, piece_colour, piece_count)

    def get_move(self, board):

        """Must be implemented by subclasses. Returns a Move object for the AI player to make"""

        raise NotImplementedError("AI opponent classes must have a get_move method")


class EasyAIPlayer(AIPlayer):

    """An Easy AI opponent that inherits from the AIPlayer class and implements the get_move method"""

    def __init__(self, piece_colour, piece_count):
        super().__init__("Easy AI", piece_colour, piece_count)
    
    def get_move(self, board):
        
        """Uses a greedy algorithm to make moves. It will capture if possible and otherwise will move pieces towards the corner if possible. Else it will make a random move"""

        corner_move_lst = []
        shuffled_board = shuffle_2D_array(board.get_board_state())

        for row in shuffled_board:
            for loc in row:
                if (loc.get_colour() == self.get_colour()):
                    move = board.get_loc_single_capture(loc)

                    if move: # capture possible with piece at loc
                        return move
                    
                    move = board.get_corner_move(loc)

                    if move: # corner move possible with piece at loc
                        corner_move_lst.append(move)

        if len(corner_move_lst) > 0: # checks if no captures are found
            return random.choice(corner_move_lst)

        return board.get_random_normal_move()


class MediumAIPlayer(AIPlayer):

    """A Medium AI opponent that inherits from the AIPlayer class and implements the get_move method"""
    
    def __init__(self, piece_colour, piece_count):
        super().__init__("Medium AI", piece_colour, piece_count)

    def get_move(self, board):

        """Uses the Monte Carlo Tree Search algorithm to make moves. The algorithm is run for 30 seconds per move"""
        
        game_tree = GameTree(board)
        return game_tree.get_next_move()

    
class HardAIPlayer(AIPlayer):

    """A Hard AI opponent that inherits from the AIPlayer class and implements the get_move method"""
        
    def __init__(self, piece_colour, piece_count):
        super().__init__("Hard AI", piece_colour, piece_count)

    def get_move(self, board):

        """Uses the Monte Carlo Tree Search algorithm to make moves. The algorithm is run for 50 seconds per move"""

        pass




    