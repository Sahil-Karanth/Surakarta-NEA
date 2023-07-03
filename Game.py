from Player import Player
from Board import Board


class Game:

    def __init__(self):
        self.__player1 = Player("TEST1")
        self.__player2 = Player("TEST2")
        self.game_over = False
        self.__board = Board()

    def set_game_over(self):
        game_status = True
        if not(self.__board.get_piece_count("player1") == 0 or self.__board.get_piece_count("player2") == 0):
            game_status = False
        
        for loc in self.__board.get_board():
            if self.__board.check_has_legal_moves(loc):
                game_status = False

        self.game_over = game_status    

    def get_board(self):
        return self.__board.get_board()

    def get_winner(self):
        if self.check_game_over() == True:
            if self.__board.get_piece_count("player1") > self.__board.get_piece_count("player2"):
                return self.__player1
            
            elif self.__board.get_piece_count("player2") > self.__board.get_piece_count("player1"):
                return self.__player2
            
            else:
                return "DRAW"
            
        return False

    def play_game(self):
        pass