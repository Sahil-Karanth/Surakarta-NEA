class Player:

    def __init__(self, piece_colour):
        self.__score = 0
        self.__piece_colour = piece_colour

    def get_score(self):
        return self.__score
    
    def update_score(self, value):
        self.__score += value
    

class HumanPlayer(Player):

    def __init__(self, name, piece_colour):
        super().__init__(piece_colour)
        self.__name = name

    def get_name(self):
        return self.__name


    