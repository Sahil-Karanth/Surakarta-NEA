from Piece import Piece

class LoopedTrack:

    """An implementation of a circular list data structure used for the board's two looped tracks.
    LoopedTrack objects contain GridLocation objects as elements and can be traversed in either direction.
    
    ####################################################################
    CLASS A SKILL: Circular list data structure
    CLASS A SKILL: Complex OOP model with encapsulation and composition
    ####################################################################
    
    """

    def __init__(self, grid_location_lst, name):

        # underlying list to store the data
        self.__lst = grid_location_lst

        # name of the LoopedTrack
        self.__name = name

        # length of the LoopedTrack
        self.__length = len(self.__lst)

        # pointers to keep track of the current location in the LoopedTrack for right and left traversal
        self.__right_pointer = 0
        self.__left_pointer = 0

    def __str__(self):
        data = [(loc.get_cords(), loc.get_piece_colour()) for loc in self.__lst]
        return str(data)
    
    def get_length(self):
        return self.__length
    
    def get_name(self):
        return self.__name

    def set_pointer(self, index, pointer_type):

        """sets the specified pointer's location to the given index.
        Values returned by get_next_left() and get_next_right() will be affected by this change"""

        # making sure index is in the range of the list (negative indexes are allowed)
        if (index * -1) <= len(self.__lst) and index < len(self.__lst):
            if pointer_type == "left":
                self.__left_pointer = index
            elif pointer_type == "right":
                self.__right_pointer = index
        else:
            raise IndexError("Index out of range. Index must be less than or equal to the length of the list.")

    def get_next_right(self):

        """returns the next item in the circular list, starting from the right pointer."""

        item = self.__lst[self.__right_pointer]
        self.__right_pointer = (self.__right_pointer + 1) % len(self.__lst)
        return item

    def get_next_left(self):

        """returns the next item in the circular list, starting from the left pointer."""

        item = self.__lst[self.__left_pointer]
        self.__left_pointer = (self.__left_pointer - 1) % len(self.__lst)
        return item
    
    def __get_all_occurence_indexes(self, cords):

        """returns a list of all the indexes that a location with the specified cords is found in lst"""

        ind_lst = []

        for ind, grid_loc in enumerate(self.__lst):
            if grid_loc.get_cords() == cords:
                ind_lst.append(ind)

        return ind_lst
    
    def switch_piece_positions(self, loc1, loc2):

        """replaces all occurences of loc1's piece with loc2's piece and all occurences of loc2's piece with loc1's piece"""

        # get all the indexes of loc1 and loc2 in the LoopedTrack
        loc1_ind_lst = self.__get_all_occurence_indexes(loc1.get_cords())
        loc2_ind_lst = self.__get_all_occurence_indexes(loc2.get_cords())

        # replace all occurences of loc1's piece with loc2's piece and vice versa
        for i in loc1_ind_lst:
            self.__lst[i].set_piece(loc2.get_piece())

        for i in loc2_ind_lst:
            self.__lst[i].set_piece(loc1.get_piece())

    def remove_piece(self, cords):

        """replaces all occurences of a piece at cords with None"""

        ind_lst = self.__get_all_occurence_indexes(cords)

        for i in ind_lst:
            self.__lst[i].set_piece(None)

    def update_piece(self, cords, piece_colour):

        """replaces all occurences of the piece at the GridLocation specified by cords's piece with a piece of the specified colour"""

        ind_lst = self.__get_all_occurence_indexes(cords)

        for i in ind_lst:
            if piece_colour == None:
                self.__lst[i].set_piece(None)
            else:
                self.__lst[i].set_piece(Piece(piece_colour))