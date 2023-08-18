class CircularList:

    """The data structure used for the board's two loops.
    Circular Lists can be traversed in either direction."""

    def __init__(self, lst):
        self.__lst = lst
        self.__length = len(lst)
        self.__right_pointer = 0
        self.__left_pointer = 0

    def __str__(self):
        return str(self.__lst)
    
    def get_lst_TEST(self):
        return self.__lst
    
    def get_length(self):
        return self.__length

    def set_pointer(self, index, pointer_type):

        """sets the specified pointer's location to the given index.
        Values returned by get_next_left() and get_next_right() will be affected by this change"""

        if (index * -1) <= len(self.__lst):
            if pointer_type == "left":
                self.__left_pointer = index
            elif pointer_type == "right":
                self.__right_pointer = index
        else:
            raise IndexError("Index out of range. Index must be less than or equal to the length of the list.")

    def get_next_right(self):

        """returns the next item in the list, starting from the right pointer."""

        item = self.__lst[self.__right_pointer]
        self.__right_pointer = (self.__right_pointer + 1) % len(self.__lst)
        return item

    def get_next_left(self):

        """returns the next item in the list, starting from the left pointer."""

        item = self.__lst[self.__left_pointer]
        self.__left_pointer = (self.__left_pointer - 1) % len(self.__lst)
        return item
    
    def __get_all_occurence_indexes(self, lst, item):

        """returns a list of all the indexes that item is found in lst"""

        ind_lst = []
        for i,n in enumerate(lst):
            if n.get_cords() == item.get_cords():
                ind_lst.append(i)

        return ind_lst
    
    def switch_positions(self, pos1, pos2):

        """replaces all occurences of pos1's piece with pos2's piece and all occurences of pos2's piece with pos1's piece"""

        pos1_ind_lst = self.__get_all_occurence_indexes(self.__lst, pos1)
        pos2_ind_lst = self.__get_all_occurence_indexes(self.__lst, pos2)

        for i in pos1_ind_lst:
            self.__lst[i].set_piece(pos2.get_piece())

        for i in pos2_ind_lst:
            self.__lst[i].set_piece(pos1.get_piece())


    def remove_piece(self, val):

        """replaces all occurences of val's piece with None"""

        ind_lst = self.__get_all_occurence_indexes(self.__lst, val)

        for i in ind_lst:
            self.__lst[i].set_piece(None)
