from Game import Game
from utility_functions import oneD_to_twoD_array
import re
from BoardConstants import BoardConstants

class Terminal_UI:
    
    def __init__(self):
        self.__UI_type = "TERMINAL"
        self.__game = self.__setup_game()

    def __setup_game(self):
        # player1name = input("Enter player 1's name: ")
        # player2name = input("Enter player 2's name: ")
        # TEST CODE
        player1name = f"Player 1 ({BoardConstants.PLAYER_1_COLOUR})"
        player2name = f"Player 2 ({BoardConstants.PLAYER_2_COLOUR})"
        # END TEST CODE
        return Game(player1name, player2name)
    
    def get_UI_type(self):
        return self.__UI_type
    
    def get_cords_from_user(self, prompt):
        valid = False
        pattern = r'^[0-5],[0-5]$'
        while not valid:
            choice = input(prompt)
            if bool(re.match(pattern, choice)):
                valid = True
            else:
                print("Invalid Coordinate. Must be of the form 'r,c' where r and c are integers between 0 and 5 inclusive.")

        return tuple([int(i) for i in choice.split(",")])

    def get_piece_colour(self, piece):
        return piece.get_colour()
    
    def display_board(self):
        board = self.__game.get_board_state()
        
        disp_board = []
        for row in board:
            for loc in row:
                if loc.is_empty():
                    disp_board.append(f"{'.'}")
                else:
                    disp_board.append(loc.get_colour())
        
        disp_board = oneD_to_twoD_array(disp_board, BoardConstants.MAX_ROW_INDEX + 1)

        self.__display_row_indexes()

        for i,row in enumerate(disp_board):
            print(f"{i} | ", end=" ")
            print("  ".join(row))

    def __display_row_indexes(self):
        print("     ", end="")
        print("  ".join([str(i) for i in range(BoardConstants.MAX_ROW_INDEX + 1)]))
        print("    ", end="")
        print("—" * 17)

    def display_winner(self):
        winner = self.__game.get_winner()
        print(f"{winner.get_name()} won!")

    def get_move_type(self):
        valid = False
        while not valid:
            move_type = input("Enter 'move' for an ordinary move to an adjacent position or 'capture' for a capturing move: ")
            if move_type == "move" or move_type == "capture":
                valid = True
            else:
                print("Invalid move type. Please try again.")
        return move_type

    def play_game(self):

        while not self.__game.is_game_over():
            self.display_board()
            print()
            print(f"{self.__game.get_current_player_name()}'s turn.")
            print()

            valid = False
            while not valid:

                move_type = self.get_move_type()
                # # TEST CODE
                # move_type = "capture"
                # # END TEST CODE

                start_cords = self.get_cords_from_user("Enter a row and column pair in the format r,c for the piece you want to move: ")
                end_cords = self.get_cords_from_user("Enter a row and column pair in the format r,c for where you want to move to: ")
                
                # # TEST CODE
                # start_cords = (2,4)
                # end_cords = (4,4)
                # # END TEST CODE

                start_loc = self.__game.get_board_state()[start_cords[0]][start_cords[1]]
                end_loc = self.__game.get_board_state()[end_cords[0]][end_cords[1]]

                if self.__game.is_legal_move(start_loc, end_loc, move_type):
                    valid = True
                else:
                    print("Invalid move. Please try again.")

            self.__game.move_piece(start_loc, end_loc, move_type)
            
            self.__game.switch_current_player()
            
            if move_type == "capture":
                self.__game.set_game_status()

        self.display_board()
        self.display_winner()
      