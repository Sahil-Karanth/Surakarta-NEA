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
        
        

        return False
    
    def get_winner(self):
        if self.__board.get_piece_count("player1") == 0:
            return self.__player2
        elif self.__board.get_piece_count("player2") == 0:
            return self.__player1
        
        return None

    def play_game(self):
        pass