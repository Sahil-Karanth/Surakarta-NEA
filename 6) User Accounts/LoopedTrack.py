from Piece import Piece

class LoopedTrack:

    """An implementation of a circular list data structure used for the board's two looped tracks.
    LoopedTrack objects contain GridLocation objects as elements and can be traversed in either direction."""

    def __init__(self, grid_location_lst):

        # underlying list to store the data
        self.__lst = grid_location_lst

        # length of the LoopedTrack
        self.__length = len(self.__lst)

        # pointers to keep track of the current location in the LoopedTrack for right and left traversal
        self.__right_pointer = 0
        self.__left_pointer = 0

    def __str__(self):
        return str(self.__lst)
    
    def get_lst_TEST(self): # ! DELETE ME
        return self.__lst
    
    def get_length(self):
        return self.__length

    def set_pointer(self, index, pointer_type):

        """sets the specified pointer's location to the given index.
        Values returned by get_next_left() and get_next_right() will be affected by this change"""

        # making sure index is in the range of the list (negative indexes are allowed)
        if (index * -1) <= len(self.__lst):
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
    
    def switch_piece_positions(self, pos1, pos2):

        """replaces all occurences of pos1's piece with pos2's piece and all occurences of pos2's piece with pos1's piece"""

        # get all the indexes of pos1 and pos2 in the LoopedTrack
        pos1_ind_lst = self.__get_all_occurence_indexes(pos1.get_cords())
        pos2_ind_lst = self.__get_all_occurence_indexes(pos2.get_cords())

        # replace all occurences of pos1's piece with pos2's piece and vice versa
        for i in pos1_ind_lst:
            self.__lst[i].set_piece(pos2.get_piece())

        for i in pos2_ind_lst:
            self.__lst[i].set_piece(pos1.get_piece())

    def remove_piece(self, cords):

        """replaces all occurences of a piece at cords with None"""

        ind_lst = self.__get_all_occurence_indexes(cords)

        for i in ind_lst:
            self.__lst[i].set_piece(None)

    def update_piece(self, cords, piece_colour):

        """replaces all occurences of val's piece with a piece of the specified colour"""

        ind_lst = self.__get_all_occurence_indexes(cords)

        for i in ind_lst:
            if piece_colour == None:
                self.__lst[i].set_piece(None)
            else:
                self.__lst[i].set_piece(Piece(piece_colour))