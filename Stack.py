class Stack:

    """Implements a stack data structure
    
    ####################################################################
    CLASS A SKILL: Stack data structure
    ####################################################################

    """

    def __init__(self):
        self.__stack = []

    def __str__(self):
        return str(self.__stack)

    def push(self, item):
        self.__stack.append(item)

    def pop(self):
        return self.__stack.pop()
    
    def peek(self):
        return self.__stack[-1]
    
    def is_empty(self):
        return len(self.__stack) == 0