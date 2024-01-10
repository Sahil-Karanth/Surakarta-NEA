class Piece:

    """A class to represent a piece's colour on the Surakarta board"""

    def __init__(self, colour):
        self.__colour = colour

    def __str__(self):
        return str(self.__colour)
    
    def get_piece_colour(self):
        return self.__colour
    


    
