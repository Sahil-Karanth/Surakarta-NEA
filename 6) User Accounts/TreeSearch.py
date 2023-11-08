import math
import random
from BoardConstants import BoardConstants
import time
import sys
from copy import deepcopy
from multiprocessing.dummy import Pool


# ! change formula name to UCT because I'm not using UCB1


# ! 10 SECOND NUM ITERATION TESTS --> done first move of a fresh game
    # before changes --> 18 iterations



class Node:

    def __init__(self, board, current_player_colour, depth, move_obj=None, is_hint=False):
        self.__board = board
        self.__move_obj = move_obj # the move that led to this node
        self.__value = 0
        self.__visited_count = 0
        self.__children = []
        self.__parent = None
        # self.__next_legal_moves = self.__set_next_legal_moves()
        self.__next_legal_moves = self.__board.get_legal_moves(current_player_colour)
        self.__depth = depth

    def get_board(self):
        return deepcopy(self.__board) # copy is used to prevent the original board from being changed

    def add_child(self, child):
        self.__children.append(child)
        child.set_parent(self)

    def set_parent(self, parent):
        self.__parent = parent

    def __set_next_legal_moves(self):

        cached_legal_moves = self.__board.get_legal_moves_cached()

    def get_parent(self):
        return self.__parent
    
    def get_depth(self):
        return self.__depth
    
    def get_move_obj(self):
        return self.__move_obj
    
    def get_visited_count(self):
        return self.__visited_count
    
    def increase_visited_count(self, num_parallel_rollouts=1):
        self.__visited_count += num_parallel_rollouts
    
    def get_children(self):
        return self.__children
    
    def get_value(self):
        return self.__value
    
    def update_value(self, value):
        self.__value += value
    
    def get_next_legal_moves(self):
        return self.__next_legal_moves
    

class GameTree:

    LOSS = -1
    DRAW = 0
    WIN = 1
    TIME_FOR_MOVE = 10 # seconds
    MOVES_PER_ROLLOUT = 200
    EXPLORATION_CONSTANT = 2

    def __init__(self, root_board):
        self.__root = Node(root_board, BoardConstants.player_2_colour, depth=0)
        self.__current_tree_depth = 0 # the maximum depth of a node in the tree
        self.__current_node = self.__root
        self.__rollout_board = None # used with rollouts
        self.__num_rollouts = 0

    def __get_current_player_colour(self, depth):

        if depth % 2 == 0: # if the depth is even, it's player 2's turn
            return BoardConstants.player_2_colour
        
        elif depth % 2 == 1:
            return BoardConstants.player_1_colour

    def add_node(self, child_board, move_obj):
        """adds a node to the tree"""

        new_depth = self.__current_node.get_depth() + 1
        current_player_colour = self.__get_current_player_colour(new_depth)

        child = Node(child_board, current_player_colour, move_obj=move_obj, depth=new_depth)

        self.__current_node.add_child(child)

        print("added child node with depth: ", child.get_depth())


    def UCB1(self, node):
        
        """returns the UCB1 value of a node"""
        
        if node.get_parent() == None:
            return 0

        else:

            try:
                return (node.get_value() / node.get_visited_count()) + math.sqrt(GameTree.EXPLORATION_CONSTANT * math.log(node.get_parent().get_visited_count()) / node.get_visited_count())
        
            except ZeroDivisionError:
                return math.inf
            

    def __check_terminal_board(self, board):
                
            if board.get_piece_count(1) == 0:
                return GameTree.WIN
            
            elif board.get_piece_count(2) == 0:
                return GameTree.LOSS
            
            return False
            

    def __get_early_stop_rollout_state(self, board):

        if board.get_piece_count(1) > self.__rollout_board.get_piece_count(2):
            return GameTree.LOSS
        
        elif board.get_piece_count(1) < self.__rollout_board.get_piece_count(2):
            return GameTree.WIN
        
        else:
            return GameTree.DRAW



    def current_is_leaf(self):

        return len(self.__current_node.get_children()) == 0
    
    def select_new_current(self):

        """sets the current node to the best child of the current node"""

        ucb1_scores = [(node, self.UCB1(node)) for node in self.__current_node.get_children()]

        self.__current_node = max(ucb1_scores, key=lambda x: x[1])[0]


        if self.__current_tree_depth < self.__current_node.get_depth():
            self.__current_tree_depth = self.__current_node.get_depth()


    def node_expansion(self):

        """expands the current node"""

        for move_obj in self.__current_node.get_next_legal_moves():
            board = self.__current_node.get_board()
            board.move_piece(move_obj)
            self.add_node(board, move_obj)

    def multiprocess_rollouts(self):

        pool = Pool(processes=3)
        
        rollout_results_lst = []

        with pool as p:
            for _ in range(3):
                rollout_result = p.apply_async(self.rollout)
                rollout_results_lst.append(rollout_result)

            p.close()
            p.join()

        return rollout_results_lst
    
    def rollout(self):

        self.__rollout_board = deepcopy(self.__current_node.get_board())
        num_moves = 0

        while num_moves < GameTree.MOVES_PER_ROLLOUT:

            terminal_board_state = self.__check_terminal_board(self.__rollout_board)
            if terminal_board_state:
                return terminal_board_state
            
            rollout_colour = self.__get_current_player_colour(self.__current_node.get_depth() + num_moves)

            move_options = self.__rollout_board.get_legal_moves(rollout_colour)
            simulated_move = random.choice(move_options)

            self.__rollout_board.move_piece(simulated_move)

            print(f"made move for {simulated_move.get_start_colour()}")
            

            num_moves += 1

        return self.__get_early_stop_rollout_state(self.__rollout_board)
            

    def backpropagate(self, results):

        result = sum([res.get() for res in results])

        node = self.__current_node

        while node != None:
            node.increase_visited_count(len(results))
            node.update_value(result)
            node = node.get_parent()

    def run_MCTS_iteration(self):

        print("NEW ITERATION")

        # ! move rollout and backprop to after the if else as it does the same thing in both cases

        while not self.current_is_leaf():
            self.select_new_current()

        if self.__current_node.get_visited_count() == 0:
            results = self.multiprocess_rollouts()
            self.backpropagate(results)
            print("rollouts complete with result: ", [i.get() for i in results])

        else:
            self.node_expansion()
            if len(self.__current_node.get_children()) != 0:
                self.__current_node = self.__current_node.get_children()[0]
            results = self.multiprocess_rollouts()
            self.backpropagate(results)
            print("rollout complete with result: ", [i.get() for i in results])

        self.__num_rollouts += len(results)

        self.__current_node = self.__root

    def get_next_move(self): # main method to call

        """returns the next move to make"""

        start_time = time.time()

        self.node_expansion()

        num_iterations = 0

        while time.time() - start_time < GameTree.TIME_FOR_MOVE:
        # while True: # ! DELETE THIS WHILE LOOP CONDITION (FOR TESTING ONLY)
            self.run_MCTS_iteration()
            num_iterations += 1

        best_node = max(self.__root.get_children(), key=lambda node: node.get_value())
        
        print(f"BEST NODE'S VALUE = {best_node.get_value()}")
        print("NUM MCTS ITERATIONS = ", num_iterations)
        print("NUM ROLLOUTS = ", self.__num_rollouts)
        print("TREE DEPTH = ", self.__current_tree_depth)

        # print("ALL IMMEDIATE CHILDREN VALUES")
        # print([(node.get_value(), node.get_move_obj().__str__()) for node in self.__root.get_children()])

        return best_node.get_move_obj()



