from Player import Player, EasyAIPlayer, MediumAIPlayer, HardAIPlayer
from Board import Board
from MultiClassBoardAttributes import MultiClassBoardAttributes
from Move import Move
from Stack import Stack


class GameNotOverError(Exception):
    pass

class Game:

    """The Game class manages the game state. It contains the board, the players, and the move history stack.
    
    ####################################################################
    CLASS A SKILL: Stack data structure (see comments in make_and_return_move and undo_and_return_move methods)
    CLASS A SKILL: Complex OOP model with encapsulation and composition
    ####################################################################

    """

    def __init__(self, player1name, player2_name, ai_level=None, game_state_string=None, player2_starts=False, player1_num_pieces=MultiClassBoardAttributes.NUM_STARTING_PIECES_EACH, player2_num_pieces=MultiClassBoardAttributes.NUM_STARTING_PIECES_EACH):

        self.__player1 = Player(player1name, MultiClassBoardAttributes.player_1_colour, player1_num_pieces)

        # If ai_level is not None, player 2 is an AI player. Otherwise, player 2 is a human player.
        if ai_level:
            self.__player2 = self.__make_ai_player(player2_name, player2_num_pieces)
        else:
            self.__player2 = Player(player2_name, MultiClassBoardAttributes.player_2_colour, player2_num_pieces)

        self.__player_tuple = (self.__player1, self.__player2)

        self.__game_over = False

        self.__board = Board(self.__player1, self.__player2, game_state_string)

        self.__move_history_stack = Stack()

        self.__current_player = self.__player1
        self.__non_current_player = self.__player2

        if player2_starts: # if a game is loaded from a save it might be player 2's turn first
            self.switch_current_player()

    def __make_ai_player(self, ai_name, player2_num_pieces):

        """Returns an AI player object using the class specified by ai_name with a piece count of player2_num_pieces"""

        difficulty_dict = {
            "Easy AI": EasyAIPlayer,
            "Medium AI": MediumAIPlayer,
            "Hard AI": HardAIPlayer,
        }

        return difficulty_dict[ai_name](MultiClassBoardAttributes.player_2_colour, player2_num_pieces)

    def get_ai_move(self):

        """Returns a Move object generated by the AI player."""

        move = self.__current_player.get_move(self.__board)

        return move

    def is_legal_move(self, start_loc, end_loc, move_type):
        return self.__board.is_legal_move(start_loc, end_loc, self.__current_player, move_type)
    
    def get_game_state_string(self):
        return self.__board.get_game_state_string()

    def set_game_status(self):

        """Sets self.__game_over to True if either player has no pieces left. A legal move can always
        be played in Surakarta, so this is the only way the game can end."""

        if (self.__player1.get_piece_count() == 0 or self.__player2.get_piece_count() == 0):
            self.__game_over = True

    def get_board_state(self):
        return self.__board.get_board_state()
    
    def is_game_over(self):
        return self.__game_over

    def get_winning_player(self):

        """Returns the Player object of the winner. If the game is not over, an exception is raised."""

        if self.is_game_over():
            if self.__player1.get_piece_count() > self.__player2.get_piece_count():
                return self.__player1
            
            elif self.__player2.get_piece_count() > self.__player1.get_piece_count():
                return self.__player2
        
        else:
            raise GameNotOverError("Attempting to get winner when game is not over.")

    def make_and_return_move(self, start_location, end_location, move_type):

        """Makes a move on the board and returns the Move object. The Move object is pushed onto the private move_history_stack attribute.
        
        ####################################################################
        CLASS A SKILL: Stack data structure (pushing onto the stack in this method)
        ####################################################################

        """

        move_obj = Move(start_location, end_location, move_type)

        # push the move onto the move history stack
        self.__move_history_stack.push(move_obj)

        # make the move on the board
        self.__board.move_piece(move_obj)

        return move_obj

    def undo_and_return_move(self):

        """Calls a method in the Board class to undo the last move made on the board and returns the Move object.
        The Move object is popped off the move_history_stack.
        
        ####################################################################
        CLASS A SKILL: Stack data structure (popping off the stack in this method)
        CLASS A SKILL: Undoing a move and passing information to the Board class's undo_move method
        ####################################################################

        """

        if self.__move_history_stack.is_empty():
            return None
    
        # pop the last move off the move history stack
        move_obj = self.__move_history_stack.pop()

        # add a piece back to the current player's piece count if the move was a capture
        if move_obj.get_move_type() == "capture":
            self.__current_player.add_piece()

        # undo the move on the board
        self.__board.undo_move(move_obj)

        return move_obj

    def get_current_player_name(self):
        return self.__current_player.get_name()
    
    def get_current_player_colour(self):
        return self.__current_player.get_piece_colour()

    def switch_current_player(self):
        self.__current_player, self.__non_current_player = self.__non_current_player, self.__current_player

    def get_player_name(self, player_number):
        return self.__player_tuple[player_number - 1].get_name()
    
    def get_player_colour(self, player_number):
        return self.__player_tuple[player_number - 1].get_piece_colour()
    
    def get_player_piece_count(self, player_number):
        return self.__player_tuple[player_number - 1].get_piece_count()