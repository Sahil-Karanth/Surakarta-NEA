from Player import Player
from Board import Board


class Game:

    def __init__(self):
        self.__player1 = Player("TEST1")
        self.__player2 = Player("TEST2")

        self.__board = Board()

    def check_game_over(self):
        pass

    def play_game(self):
        pass