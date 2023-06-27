class CircularList:

    def __init__(self, lst):
        self.__lst = lst
        self.__reverse_lst = lst[::-1]
        self.__current_index = 0

    def set_current_index(self, index):
        if (index * -1) <= len(self.__lst):
            self.__current_index = index
        else:
            raise IndexError("Index out of range. Index must be less than or equal to the length of the list.")

    def get_next_right(self):
        item = self.__lst[self.__current_index]
        self.__current_index = (self.__current_index + 1) % len(self.__lst)
        return item

    def get_next_left(self):
        item = self.__reverse_lst[self.__current_index]
        self.__current_index = (self.__current_index + 1) % len(self.__reverse_lst)
        return item
