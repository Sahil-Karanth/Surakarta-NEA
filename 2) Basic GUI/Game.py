from Player import HumanPlayer
from Board import Board
from BoardConstants import BoardConstants

class Game:

    def __init__(self, player1name, player2name):
        self.__player1 = HumanPlayer(player1name, BoardConstants.PLAYER_1_COLOUR)
        self.__player2 = HumanPlayer(player2name, BoardConstants.PLAYER_2_COLOUR)
        self.__game_over = False
        self.__board = Board()
        self.__current_player = self.__player1
        self.__non_current_player = self.__player2

    def is_legal_move(self, start_loc, end_loc, move_type):
        return self.__board.is_legal_move(start_loc, end_loc, self.__current_player, move_type)

    def set_game_status(self):

        """Sets self.__game_over to True if either player has no pieces left. A legal move can always
        be played in Surakarta, so this is the only way the game can end."""

        if (self.__board.get_piece_count("player1") == 0 or self.__board.get_piece_count("player2") == 0):
            self.__game_over = True
            return

    def get_board_state(self):
        return self.__board.get_board_state()
    
    def is_game_over(self):
        return self.__game_over

    def get_winner(self):
        if self.is_game_over() == True:
            if self.__board.get_piece_count("player1") > self.__board.get_piece_count("player2"):
                return self.__player1
            
            elif self.__board.get_piece_count("player2") > self.__board.get_piece_count("player1"):
                return self.__player2
            
            else:
                return None
            
        return False

    def move_piece(self, start_location, end_location, move_type):
        self.__board.move_piece(start_location, end_location, move_type)

    # def capture_piece(self, start_location, end_location):
    #     self.__board.capture_piece(start_location, end_location)

    def get_current_player_name(self):
        return self.__current_player.get_name()
    
    def switch_current_player(self):
        self.__current_player, self.__non_current_player = self.__non_current_player, self.__current_player

    def get_player1_name(self):
        return self.__player1.get_name()
    
    def get_player2_name(self):
        return self.__player2.get_name()
    
    def get_player1_colour(self):
        return self.__player1.get_colour()
    
    def get_player2_colour(self):
        return self.__player2.get_colour()