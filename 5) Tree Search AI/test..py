from Board import Board
from Player import HumanPlayer
from BoardConstants import BoardConstants
from TreeSearch import GameTree
from copy import deepcopy


# ! TEST USING THIS FILE
    # the child_node's legal moves for some reason still use the green piece when it should be a yellow move


player1 = HumanPlayer("player1", BoardConstants.PLAYER_1_COLOUR)
player2 = HumanPlayer("player2", BoardConstants.PLAYER_2_COLOUR)

board = Board(player1, player2)
board_copy = deepcopy(board)

tree = GameTree(board)

root = tree.get_root_TEST()

for row in board.get_board_state():
    print([i.get_colour() for i in row])

print(root.get_next_legal_states()[6])

move_obj = root.get_next_legal_states()[6]
board_copy.move_piece(move_obj)

tree.add_node(board_copy, move_obj)

child_node = root.get_children()[0]

print(child_node.get_next_legal_states()[0])