from Piece import Piece
from BoardConstants import BoardConstants

class GridLocation:

    """represnts information about a location on the board such as
    the piece on it and its coordinates"""

    def __init__(self, cords):
        self.__cords = cords

        # initial values set for a fresh board
        self.__piece = self.__set_initial_piece()
        self.__loop = self.__set_loop()

    def __set_loop(self):

        """determines which loop a location sits on"""

        # outer loop cordinates have row (2 or 3) and column (2 or 3) etc
        OUTER_LOOP_NUMBERS = (2, 3)
        INNER_LOOP_NUMBERS = (1, 4)

        if (self.__cords[0] in OUTER_LOOP_NUMBERS and self.__cords[1] in INNER_LOOP_NUMBERS) or (self.__cords[0] in INNER_LOOP_NUMBERS and self.__cords[1] in OUTER_LOOP_NUMBERS):
            return "BOTH"

        elif INNER_LOOP_NUMBERS[0] in self.__cords or INNER_LOOP_NUMBERS[1] in self.__cords:
            return "INNER"
        
        elif OUTER_LOOP_NUMBERS[0] in self.__cords or OUTER_LOOP_NUMBERS[1] in self.__cords:
            return "OUTER"
        
        else:
            return None

    def __set_initial_piece(self):

        """determines which piece should be placed on a location at the start"""

        if self.__cords[0] in BoardConstants.PLAYER_1_ROWS:
            return Piece(BoardConstants.PLAYER_1_COLOUR)
        
        elif self.__cords[0] in BoardConstants.PLAYER_2_ROWS:
            return Piece(BoardConstants.PLAYER_2_COLOUR)

        else:
            return None

    def is_empty(self):
        return self.__piece == None
    
    def set_piece(self, piece):
        self.__piece = piece

    def get_piece(self):
        return self.__piece
    
    def get_colour(self):
        if self.__piece == None:
            return None
        else:
            return self.__piece.get_colour()
    
    def get_cords(self):
        return self.__cords
    
    def get_loop(self):
        return self.__loop
