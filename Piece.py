class Piece:

    Next_Piece_ID = 0

    def __init__(self, colour):
        self.__id = Piece.Next_Piece_ID
        Piece.Next_Piece_ID += 1
        self.__colour = colour
    
    def get_piece_id(self):
        return self.__id
    
    def get_colour(self):
        return self.__colour
    


    
