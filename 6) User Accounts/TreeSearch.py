import math
import random
from BoardConstants import BoardConstants
import time
import sys
from copy import deepcopy
from multiprocessing import cpu_count
# from multiprocessing import Pool
from multiprocessing.dummy import Pool

# need a better evaluation function because there are many more moves than just capturing pieces so need to differentiate between positions
# with the same number of pieces

# ! 10 SECOND NUM ITERATION TESTS --> done first move of a fresh game
#     multiprocess: 12 iterations, 36 rollouts
#     single process: 25, 25
#     muiltithread: 9 iterations, 27 rollouts


# rollout timing tests
    # 35.661699056625366 out of 45 seconds spent in rollouts
    # 104.00432991981506 out of 120 seconds spent in rollouts
    # 48.94266414642334 out of 60 seconds spent in rollouts

# num iterations tests
    # from base board
        # 45 seconds: 103, 95, 108, 104





class Node:

    def __init__(self, board, current_player_colour, depth, move_obj=None, is_hint=False):
        self.__board = board
        self.__move_obj = move_obj # the move that led to this node
        self.__value = 0
        self.__visited_count = 0
        self.__children = []
        self.__parent = None
        # self.__next_legal_moves = self.__set_next_legal_moves()
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
    TIME_FOR_MOVE = 20 # seconds
    MOVES_PER_ROLLOUT = 2000
    EXPLORATION_CONSTANT = 1.414
    NUM_PARALLEL_ROLLOUTS = 3

    def __init__(self, root_board):
        self.__root = Node(root_board, BoardConstants.player_2_colour, depth=0)
        self.__current_tree_depth = 0 # the maximum depth of a node in the tree
        self.__current_node = self.__root
        self.__rollout_board = None # used with rollouts
        self.__num_rollouts = 0
        self.__time_in_rollouts = 0 # seconds
        self.__node_count = 1 # number of nodes in the tree

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

        # print("added child node with depth: ", child.get_depth())


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

        if board.get_piece_count(1) > board.get_piece_count(2):
            return GameTree.LOSS
        
        elif board.get_piece_count(1) < board.get_piece_count(2):
            return GameTree.WIN
        
        else:
            return GameTree.DRAW
        
    def __get_current_legal_moves(self):
        board = self.__current_node.get_board()
        current_player_colour = self.__get_current_player_colour(self.__current_node.get_depth())
        return board.get_legal_moves(current_player_colour)


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

        legal_moves = self.__get_current_legal_moves()

        for move_obj in legal_moves:
            self.__node_count += 1
            board = self.__current_node.get_board()
            board.move_piece(move_obj)
            self.add_node(board, move_obj)


    def multiprocess_rollouts(self):

        pool = Pool(processes=GameTree.NUM_PARALLEL_ROLLOUTS)
        
        rollout_results_lst = []
        with pool as p:
            for _ in range(GameTree.NUM_PARALLEL_ROLLOUTS):
                rollout_result = p.apply_async(self.rollout, (deepcopy(self.__current_node.get_board()), ))
                rollout_results_lst.append(rollout_result)

            p.close()
            p.join()

        return rollout_results_lst
    
    def rollout(self, rollout_board):
        
        start_time = time.time()

        # self.__rollout_board = deepcopy(self.__current_node.get_board())
        num_moves = 0

        while num_moves < GameTree.MOVES_PER_ROLLOUT:

            terminal_board_state = self.__check_terminal_board(rollout_board)
            if terminal_board_state:
                print(f"rollout ended after {num_moves} moves")
                return terminal_board_state
            
            rollout_colour = self.__get_current_player_colour(self.__current_node.get_depth() + num_moves)

            move_options = rollout_board.get_legal_moves(rollout_colour)
            simulated_move = random.choice(move_options)

            rollout_board.move_piece(simulated_move)

            # print(f"made move for {simulated_move.get_start_colour()}")
            

            num_moves += 1

        end_time = time.time()

        self.__time_in_rollouts += end_time - start_time

        print(f"rollout ended after {num_moves} moves")
        return self.__get_early_stop_rollout_state(rollout_board)
            

    def backpropagate_multiple(self, results):

        result = sum([res.get() for res in results])

        node = self.__current_node

        while node != None:
            node.increase_visited_count(len(results))
            node.update_value(result)
            node = node.get_parent()


    def backpropagate(self, result):

        node = self.__current_node

        while node != None:
            node.increase_visited_count()
            node.update_value(result)
            node = node.get_parent()


    def run_MCTS_iteration(self):

        # print("NEW ITERATION")

        # ! move rollout and backprop to after the if else as it does the same thing in both cases

        while not self.current_is_leaf():
            self.select_new_current()

        if self.__current_node.get_visited_count() == 0:
            # results = self.multiprocess_rollouts()
            result = self.rollout(deepcopy(self.__current_node.get_board()))
            # print(f"end of rollouts and player 1 has {self.__current_node.get_board().get_piece_count(1)} pieces and player 2 has {self.__current_node.get_board().get_piece_count(2)} pieces")
            # self.backpropagate(results)
            self.backpropagate(result)
            # print("rollouts complete with result: ", [i.get() for i in results])

        else:
            self.node_expansion()
            if len(self.__current_node.get_children()) != 0:
                self.__current_node = self.__current_node.get_children()[0]
            # results = self.multiprocess_rollouts()
            result = self.rollout(deepcopy(self.__current_node.get_board()))
            # self.backpropagate_multiple(results)
            self.backpropagate(result)
            # print("rollout complete with result: ", [i.get() for i in results])

        # self.__num_rollouts += len(results)
        self.__num_rollouts += 1

        self.__current_node = self.__root


    def get_next_move(self): # main method to call

        """returns the next move to make"""

        avg_time_for_single_iteration = 0
        start_time = time.time()

        self.node_expansion()

        num_iterations = 0

        while time.time() - start_time < GameTree.TIME_FOR_MOVE:
        # while True: # ! DELETE THIS WHILE LOOP CONDITION (FOR TESTING ONLY)
            self.run_MCTS_iteration()
            num_iterations += 1
            avg_time_for_single_iteration += (time.time() - start_time) / num_iterations


        best_node = max(self.__root.get_children(), key=lambda node: node.get_value())
        
        print(f"MCTS RAN FOR: {GameTree.TIME_FOR_MOVE} SECONDS")
        print(f"BEST NODE'S VALUE = {best_node.get_value()}")
        print("NUM MCTS ITERATIONS = ", num_iterations)
        print("NUM ROLLOUTS = ", self.__num_rollouts)
        print("MAX TREE DEPTH = ", self.__current_tree_depth)
        print("TIME IN ROLLOUTS = ", self.__time_in_rollouts)
        print("NUM NODES IN TREE = ", self.__node_count)

        print("ALL IMMEDIATE CHILDREN VALUES")
        print([(node.get_value(), node.get_move_obj().__str__()) for node in self.__root.get_children()])

        return best_node.get_move_obj()



