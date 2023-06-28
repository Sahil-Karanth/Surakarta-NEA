class Player:

    def __init__(self):
        self.__score = 0

    def get_name(self):
        return self.__name
    
    def set_name(self, name):
        self.__name = name

    def get_score(self):
        return self.__score
    

class HumanPlayer(Player):

    def __init__(self, name):
        super().__init__()
        self.__name = name

    


    