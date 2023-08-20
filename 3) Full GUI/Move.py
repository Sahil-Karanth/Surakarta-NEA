class Move:

    """Represents a move made which is pushed to the move history stack"""

    def __init__(self, start_loc, end_loc, move_type):
        self.__start_loc = start_loc
        self.__end_loc = end_loc
        self.__move_type = move_type
        # self.__colour = end_loc.get_colour()
        # print("PRINTING COLOUR")
        # print(self.__colour)

    def __str__(self):
        return f"{self.__move_type} from {self.__start_loc.get_cords()} to {self.__end_loc.get_cords()}"
    
    def get_start_loc(self):
        return self.__start_loc
    
    def get_end_loc(self):
        return self.__end_loc

    def get_move_type(self):
        return self.__move_type