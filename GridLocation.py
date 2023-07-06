from Piece import Piece

class GridLocation:

    EDGE_CORDS = ((0, 0), (0, 5), (5, 0), (5, 5))

    def __init__(self, cords):
        self.__cords = cords
        self.__piece = self.__set_initial_piece()
        self.__loop = self.__set_loop()
        self.__loop_index = self.__set_loop_index()

    def __set_loop_index(self):
        if (0 in self.__cords or 5 in self.__cords) and self.__cords not in GridLocation.EDGE_CORDS:
            self.__loop_index = True
        else:
            self.__loop_index = False

    def __set_loop(self):
        OUTER_NUMBERS = (2, 3)
        INNER_NUMBERS = (1, 4)
        if (self.__cords[0] in OUTER_NUMBERS and self.__cords[1] in INNER_NUMBERS) or (self.__cords[0] in INNER_NUMBERS and self.__cords[1] in OUTER_NUMBERS):
            return "BOTH"

        elif 1 in self.__cords or 4 in self.__cords:
            return "INNER"
        
        elif 3 in self.__cords or 2 in self.__cords:
            return "OUTER"

    def __set_initial_piece(self):
        if self.__cords[1] == 0 or self.__cords[1] == 1:
            return Piece("B")
        
        elif self.__cords[1] == 4 or self.__cords[1] == 5:
            return Piece("G")

        else:
            return None

    def is_empty(self):
        return self.piece == None
    
    def set_piece(self, piece):
        self.__piece = piece

    def get_piece(self):
        return self.__piece
    
    def get_cords(self):
        return self.__cords
    
    def get_loop(self):
        return self.__loop
    
    def is_loop_index(self):
        return self.__loop_index


