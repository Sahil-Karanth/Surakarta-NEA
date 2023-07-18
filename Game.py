from Player import HumanPlayer
from Board import Board
from GridLocation import GridLocation

class Game:

    def __init__(self, player1name, player2name):
        self.__player1 = HumanPlayer(player1name, "B") # ! FIX THIS: make sure colours are in some class or centralised
        self.__player2 = HumanPlayer(player2name, "G")
        self.__game_over = False
        self.__board = Board()
        self.__current_player = self.__player1
        self.__non_current_player = self.__player2

    def is_legal_move(self, start_loc, end_loc, move_type):
        if move_type == "move":
            return self.__board.check_normal_legal(start_loc, end_loc, self.__current_player)
        
        elif move_type == "capture":
            return self.__board.check_capture_legal(start_loc, end_loc, self.__current_player)

    def set_game_status(self):

        # ! BUG only checks for one player

        if self.__board.get_piece_count("player1") == 0 or self.__board.get_piece_count("player2") == 0:
            self.__game_over = True
            return

        for row in self.__board.get_board_state():
            for loc in row:
                if loc.get_piece() == None:
                    continue
                elif loc.get_colour() == self.__current_player.get_colour():
                    move_is_legal = self.__board.check_has_legal_moves(loc, self.__current_player)

                elif loc.get_colour() == self.__non_current_player.get_colour():
                    move_is_legal = self.__board.check_has_legal_moves(loc, self.__non_current_player)

                if move_is_legal:
                    self.__game_over = False
                    return

    def get_board_state(self):
        return self.__board.get_board_state()
    
    def get_board(self):
        return self.__board
    
    def get_game_over(self):
        return self.__game_over

    def get_winner(self):
        if self.get_game_over() == True:
            if self.__board.get_piece_count("player1") > self.__board.get_piece_count("player2"):
                return self.__player1
            
            elif self.__board.get_piece_count("player2") > self.__board.get_piece_count("player1"):
                return self.__player2
            
            else:
                return "DRAW"
            
        return False

    def move_piece(self, start_location, end_location):
        self.__board.move_piece(start_location, end_location, self.__current_player)

    def capture_piece(self, start_location, end_location):
        self.__board.capture_piece(start_location, end_location)

    def get_current_player(self):
        return self.__current_player
    
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