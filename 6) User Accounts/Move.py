class Move:

    """Represents a move in the game. Stores the start and end locations of the move, the type of move and the colour of the start and end locations. Start and end colours are stored as pieces at a location can change"""

    def __init__(self, start_loc, end_loc, move_type):
        self.__start_loc = start_loc
        self.__end_loc = end_loc
        self.__move_type = move_type
        self.__start_colour = self.__start_loc.get_colour()
        self.__end_colour = self.__end_loc.get_colour()

    def __str__(self):
        return f"{self.__move_type} from {self.__start_loc.get_cords()} to {self.__end_loc.get_cords()}"
    
    def get_start_loc(self):
        return self.__start_loc
    
    def get_end_loc(self):
        return self.__end_loc
    
    def get_start_cords(self):
        return self.__start_loc.get_cords()
    
    def get_end_cords(self):
        return self.__end_loc.get_cords()

    def get_move_type(self):
        return self.__move_type
    
    def get_start_colour(self):
        return self.__start_colour

    def get_end_colour(self):
        return self.__end_colour