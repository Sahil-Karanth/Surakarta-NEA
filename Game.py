from Player import Player
from Board import Board


class Game:

    def __init__(self):
        self.__player1 = Player("TEST1")
        self.__player2 = Player("TEST2")

        self.__board = Board()

    def check_game_over(self):
        if self.__board.get_piece_count("player1") == 0 or self.__board.get_piece_count("player2") == 0:
            return True
        
        for loc in self.__board.get_board():
            if self.__board.check_has_legal_moves(loc):
                return False

        return True
    
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