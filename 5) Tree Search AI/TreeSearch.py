import math

class Node:

    def __init__(self, board):
        self.__board = board
        self.__val = 0
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
        self.__current_node = self.__root

    def __str__(self):
        """returns each node and it's children on a new line"""


    def add_node(self, child_val):
        """adds a node to the tree"""
        child = Node(child_val)
        self.__current_node.add_child(child)
        # self.__current_node = child

    def UCB1(self, node):
        
        """returns the UCB1 value of a node"""
        
        if node.get_parent() == None:
            return 0
        else:
            return (node.get_val() / node.get_visited_count()) + math.sqrt(2 * math.log(node.get_parent().get_visited_count()) / node.get_visited_count())
        

    def current_is_leaf(self):

        return len(self.__current_node.get_children()) == 0
    

    def set_new_current(self):

        """sets the current node to the best child of the current node"""

        ucb1_scores = [(node, self.UCB1(node)) for node in self.__current_node.get_children()]

        self.__current_node = max(ucb1_scores, key=lambda x: x[1])[0]

    def node_expansion(self):

        """expands the current node"""

        for node in self.__get_legal_next_states():
            self.add_node(node)

    def __get_legal_next_states(self):

        """returns a list of legal next states form the current node"""

        




    def get_next_move(self): # ! main method to call

        """returns the next move to make"""

        pass



