from BoardConstants import BoardConstants
import random
from utility_functions import shuffle_2D_array
from TreeSearch import GameTree

class Player:

    def __init__(self, name, piece_colour):
        self.__name = name
        self.__piece_colour = piece_colour
        self.__piece_count = BoardConstants.NUM_STARTING_PIECES_EACH

    def get_colour(self):
        return self.__piece_colour
    
    def get_name(self):
        return self.__name
    
    def get_piece_count(self):
        return self.__piece_count
    
    def remove_piece(self):
        self.__piece_count -= 1
        if self.__piece_count < 0:
            raise ValueError("Player has no pieces left, cannot remove piece")
        
    def add_piece(self):

        """Adds a piece to the player's piece count. Only used to return a piece to a player after a move is undone."""

        self.__piece_count += 1
        if self.__piece_count > BoardConstants.NUM_STARTING_PIECES_EACH:
            raise ValueError("Player has too many pieces, cannot add piece")
    

class HumanPlayer(Player):

    def __init__(self, name, piece_colour):
        super().__init__(name, piece_colour)
    

class AIPlayer(Player):
    
    def __init__(self, name, piece_colour):
        super().__init__(name, piece_colour)

    def get_move(self, board):
        raise NotImplementedError("AI opponent classes must have a get_move method")


class EasyAIPlayer(AIPlayer):

    def __init__(self, piece_colour):
        super().__init__("Easy AI", piece_colour)
    
    def get_move(self, board):
        
        corner_move_lst = []
        shuffled_board = shuffle_2D_array(board.get_board_state())

        for row in shuffled_board:
            for loc in row:
                if (loc.get_colour() == self.get_colour()):
                    move = board.get_capture_with(loc)

                    if move and random.randint(0, 1) == 0: # 50% chance of capturing
                        return move
                    
                    move = board.get_corner_move(loc)

                    if move:
                        corner_move_lst.append(move)

        if len(corner_move_lst) > 0:
            return random.choice(corner_move_lst)

        return board.get_random_move()


class MediumAIPlayer(AIPlayer):
    
    def __init__(self, piece_colour):
        super().__init__("Medium AI", piece_colour)

    def get_move(self, board):
        
        game_tree = GameTree(board)
        return game_tree.get_next_move()

    
class HardAIPlayer(AIPlayer):
        
    def __init__(self, piece_colour):
        super().__init__("Hard AI", piece_colour)

    def get_move(self, board):
        pass




    