class Piece:

    def __init__(self, colour):
        self.__colour = colour

    def __str__(self):
        return str(self.__colour)
    
    def get_colour(self):
        return self.__colour
    


    