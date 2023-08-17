class Player:

    def __init__(self, piece_colour):
        self.__piece_colour = piece_colour

    def get_colour(self):
        return self.__piece_colour
    

class HumanPlayer(Player):

    def __init__(self, name, piece_colour):
        super().__init__(piece_colour)
        self.__name = name

    def get_name(self):
        return self.__name


    