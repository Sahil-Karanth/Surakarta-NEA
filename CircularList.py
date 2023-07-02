class CircularList:

    def __init__(self, lst):
        self.__lst = lst
        self.__length = len(lst)
        self.__reverse_lst = lst[::-1]
        self.__current_index = 0

    def __str__(self):
        return str(self.__lst)
    
    def get_length(self):
        return self.__length

    def set_current_index(self, index):
        if (index * -1) <= len(self.__lst):
            self.__current_index = index
        else:
            raise IndexError("Index out of range. Index must be less than or equal to the length of the list.")
        
    def get_current_index(self):
        return self.__current_index

    def get_next_right(self):
        item = self.__lst[self.__current_index]
        self.__current_index = (self.__current_index + 1) % len(self.__lst)
        return item

    def get_next_left(self):
        item = self.__reverse_lst[self.__current_index]
        self.__current_index = (self.__current_index + 1) % len(self.__reverse_lst)
        return item
    
    def replace_item(self, to_replace, replace_with): # * find better name for this method
        
        try:
            ind_to_replace = self.__get_all_occurence_indexes(self.__lst, to_replace)
            ind_to_replace = self.__get_all_occurence_indexes(self.__lst, replace_with)
        except ValueError:
            return False
        
        for a,b in zip(ind_to_replace, ind_to_replace):
            self.__lst[a] = replace_with
            self.__reverse_lst[self.__length - a - 1] = replace_with

            self.__lst[b] = None
            self.__reverse_lst[self.__length - b - 1] = None

        return True
    
    def __get_all_occurence_indexes(self, lst, item):
        ind_lst = []
        for i,n in enumerate(lst):
            if n == item:
                ind_lst.append(i)

        return ind_lst