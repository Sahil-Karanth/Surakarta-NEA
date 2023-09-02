import math

class Node:

    def __init__(self, val):
        self.__val = val
        self.__visited_count = 0
        self.__children = []
        self.__parent = None

    def add_child(self, child):
        self.__children.append(child)
        child.set_parent(self)

    def set_parent(self, parent):
        self.__parent = parent

    def get_parent(self):
        return self.__parent
    
    def get_children(self):
        return self.__children
    
    def get_val(self):
        return self.__val
    

class GameTree:

    def __init__(self, root_state):
        self.__root = Node(root_state)

    def __str__(self):
        """returns each node and it's children on a new line"""


    def add_node(self, child_val, parent_node):
        
        """adds a node to the tree"""
        
        child = Node(child_val)
        parent_node.add_child(child)

    def UCB1(self, node):
        
        """returns the UCB1 value of a node"""
        
        if node.get_parent() == None:
            return 0
        else:
            return (node.get_val() / node.get_visited_count()) + math.sqrt(2 * math.log(node.get_parent().get_visited_count()) / node.get_visited_count())


    def get_next_move(self):

        """returns the next move to make"""



