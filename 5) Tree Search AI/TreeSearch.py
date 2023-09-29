import math
import random
from BoardConstants import BoardConstants
import time
from copy import deepcopy

# ! CHECK TO MAKE SURE THE TREE IS TRYING TO MAKE THE BEST MOVE FOR THE OPPONENT AS MOVES ALTERNATE

class Node:

    def __init__(self, board, current_player_colour, move_obj=None, is_hint=False):
        self.__board = board
        self.__move_obj = move_obj # the move that led to this node
        # self.__player_turn_colour = player_turn_colour
        self.__value = 0
        self.__visited_count = self.__set_initial_count()
        self.__children = []
        self.__parent = None
        self.__next_legal_states = self.__board.get_legal_moves(current_player_colour)

    def __set_initial_count(self):
        if self.__board.get_piece_count(1) == 0 or self.__board.get_piece_count(2) == 0: # prevents rollouts of terminal states
            return math.inf
        
        else:
            return 0

    def get_board(self):
        return deepcopy(self.__board) # copy is used to prevent the original board from being changed

    def add_child(self, child):
        self.__children.append(child)
        child.set_parent(self)

    def set_parent(self, parent):
        self.__parent = parent

    def get_parent(self):
        return self.__parent
    
    def get_move_obj(self):
        return self.__move_obj
    
    def get_visited_count(self):
        return self.__visited_count
    
    def increment_visited_count(self):
        self.__visited_count += 1
    
    def get_children(self):
        return self.__children
    
    def get_value(self):
        return self.__value
    
    def increase_value(self, value):
        self.__value += value
    
    def get_next_legal_states(self):
        return self.__next_legal_states
    

class GameTree:

    LOSS = -1
    DRAW = 0
    WIN = 1
    TIME_FOR_MOVE = 2 # seconds

    def __init__(self, root_board):
        self.__current_player_colour = BoardConstants.PLAYER_2_COLOUR
        self.__root = Node(root_board, self.__current_player_colour)
        self.__current_node = self.__root
        self.__rollout_board = None # used with rollouts
        self.__current_player_colour = BoardConstants.PLAYER_2_COLOUR

        self.__switch_player_colour_map = {
            BoardConstants.PLAYER_1_COLOUR: BoardConstants.PLAYER_2_COLOUR,
            BoardConstants.PLAYER_2_COLOUR: BoardConstants.PLAYER_1_COLOUR
        }

    def __str__(self):
        """returns each node and it's children on a new line"""

    def get_root_TEST(self):
        return self.__root

    def add_node(self, child_board, move_obj):
        """adds a node to the tree"""
        child = Node(child_board, self.__current_player_colour, move_obj)
        self.__current_node.add_child(child)
        # self.__current_node = child

    def UCB1(self, node):
        
        """returns the UCB1 value of a node"""
        
        if node.get_parent() == None:
            return 0
        
        elif node.get_visited_count() == math.inf:
            return math.inf

        else:

            try:
                return (node.get_value() / node.get_visited_count()) + math.sqrt(2 * math.log(node.get_parent().get_visited_count()) / node.get_visited_count())
        
            except ZeroDivisionError:
                return math.inf

    def current_is_leaf(self):

        return len(self.__current_node.get_children()) == 0
    
    def switch_current_player_colour(self):
            
            self.__current_player_colour = self.__switch_player_colour_map[self.__current_player_colour]
    
    def select_new_current(self):

        """sets the current node to the best child of the current node"""

        # if condition is to prevent the AI from selecting a terminal state as the current node
        ucb1_scores = [(node, self.UCB1(node)) for node in self.__current_node.get_children() if node.get_visited_count() != math.inf]

        self.__current_node = max(ucb1_scores, key=lambda x: x[1])[0]


    def node_expansion(self):

        """expands the current node"""

        for move_obj in self.__current_node.get_next_legal_states():
            board = self.__current_node.get_board()
            board.move_piece(move_obj)
            self.add_node(board, move_obj)

        self.switch_current_player_colour()
    
    def rollout(self):

        moves_without_capture = 0
        self.__rollout_board = deepcopy(self.__current_node.get_board())

        self.__current_player_colour = BoardConstants.PLAYER_2_COLOUR

        simulated_move = random.choice(self.__current_node.get_next_legal_states())
        while True:

            if simulated_move.get_move_type() == "move":
                moves_without_capture += 1


            self.__rollout_board.move_piece(simulated_move)

            print(f"made move for {simulated_move.get_start_colour()}")

            if self.__rollout_board.get_piece_count(1) == 0:
                return GameTree.WIN
            
            elif self.__rollout_board.get_piece_count(2) == 0:
                return GameTree.LOSS
            
            moves_lst_testing = self.__rollout_board.get_legal_moves(self.__current_player_colour)

            simulated_move = random.choice(self.__rollout_board.get_legal_moves(self.__current_player_colour))

            self.switch_current_player_colour()
            
            # elif moves_without_capture == BoardConstants.DRAW_THRESHOLD:
            #     return GameTree.DRAW
            
    
    def backpropagate(self, result):

        node = self.__current_node

        while node != None:
            node.increment_visited_count()
            node.increase_value(result)
            node = node.get_parent()

        # ! DO I NEED TO GO BACK TO THE ROOT NODE?


    def run_MCTS_iteration(self):

        # TEST BOARD PRINT

        for row in self.__current_node.get_board().get_board_state():
            print([i.get_colour() for i in row])

        print("NEW ITERATION")
        global curr_node_testing
        curr_node_testing = self.__current_node


        while not self.current_is_leaf():
            self.select_new_current()

        if self.__current_node.get_visited_count() == 0:
            result = self.rollout()
            self.backpropagate(result)
            print("rollout complete with result: ", result)

        else:
            self.node_expansion()
            self.__current_node = self.__current_node.get_children()[0]
            result = self.rollout()
            self.backpropagate(result)
            print("rollout complete with result: ", result)


        self.__current_node = self.__root


    def get_next_move(self): # main method to call

        """returns the next move to make"""

        start_time = time.time()

        self.node_expansion()

        num_iterations = 0

        print(f"{len(self.__current_node.get_children())} POSSIBLE MOVES FIRST MOVE")

        while time.time() - start_time < GameTree.TIME_FOR_MOVE:
            self.run_MCTS_iteration()
            num_iterations += 1

        best_node = max(self.__root.get_children(), key=lambda node: node.get_value())
        
        print(f"BEST NODE'S VALUE = {best_node.get_value()}")
        print("NUM ITERATIONS = ", num_iterations)

        return best_node.get_move_obj()



