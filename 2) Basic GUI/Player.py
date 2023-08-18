from BoardConstants import BoardConstants

class Player:

    def __init__(self, piece_colour):
        self.__piece_colour = piece_colour
        self.__piece_count = BoardConstants.NUM_STARTING_PIECES_EACH

    def get_colour(self):
        return self.__piece_colour
    
    def get_piece_count(self):
        return self.__piece_count
    
    def remove_piece(self):
        self.__piece_count -= 1
        if self.__piece_count < 0:
            raise ValueError("Player has no pieces left, cannot remove piece")
    

class HumanPlayer(Player):

    def __init__(self, name, piece_colour):
        super().__init__(piece_colour)
        self.__name = name

    def get_name(self):
        return self.__name


    