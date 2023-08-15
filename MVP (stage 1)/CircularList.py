from GridLocation  import GridLocation


class CircularList:

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
        if (index * -1) <= len(self.__lst):
            if pointer_type == "left":
                self.__left_pointer = index
            elif pointer_type == "right":
                self.__right_pointer = index
        else:
            raise IndexError("Index out of range. Index must be less than or equal to the length of the list.")

    def get_next_right(self):
        item = self.__lst[self.__right_pointer]
        self.__right_pointer = (self.__right_pointer + 1) % len(self.__lst)
        return item

    def get_next_left(self):
        item = self.__lst[self.__left_pointer]
        self.__left_pointer = (self.__left_pointer - 1) % len(self.__lst)
        return item
    
    def replace_item(self, to_replace, replace_with): # * find better name for this method
        
        print("to_replace: ", to_replace)
        print("replace_with: ", replace_with)

        try:
            ind_to_replace = self.__get_all_occurence_indexes(self.__lst, to_replace)
            ind_replace_with = self.__get_all_occurence_indexes(self.__lst, replace_with)
        except ValueError:
            return False
        
        for a,b in zip(ind_to_replace, ind_replace_with):
            self.__lst[a].set_piece(replace_with.get_piece())
            self.__lst[b].set_piece(None)

        return True
    
    def __get_all_occurence_indexes(self, lst, item):
        ind_lst = []
        for i,n in enumerate(lst):
            if n.get_cords() == item.get_cords():
                ind_lst.append(i)

        return ind_lst




# class Test:

#     def __init__(self, a):
#         self.a = a



# lst = [
#     GridLocation((0,0)),
#     GridLocation((0,1)),
#     GridLocation((5,5)),
# ]

# lst = CircularList(lst)

# print("BEFORE")
# for i in lst.get_lst_TEST():
#     print(i.get_cords(), i.get_colour())

# lst.replace_item(GridLocation((0,0)), GridLocation((5,5)))

# print("AFTER")
# for i in lst.get_lst_TEST():
#     print(i.get_cords(), i.get_colour())