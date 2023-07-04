from Game import Game
from utility_functions import oneD_to_twoD_array

class Terminal_UI:
    
    def __init__(self):
        self.__UI_type = "TERMINAL"
        self.__game = Game()

    def get_UI_type(self):
        return self.__UI_type
    
    def get_user_piece_to_move(self):
        choice = input("Enter a row and column pair in the format r,c for the piece you want to move: ")
        return choice
    
    def get_user_piece_moving_to(self):
        choice = input("Enter a row and column pair in the format r,c for where you want to move to: ")
        return choice
    
    def get_piece_colour(self, piece):
        return piece.get_colour()
    
    def display_board(self):
        board = self.__game.get_board()
        
        disp_board = []
        for row in board:
            for loc in row:
                if loc.get_piece() == None:
                    disp_board.append(f"{'.'}")
                else:
                    disp_board.append(loc.get_piece().get_colour())
        
        disp_board = oneD_to_twoD_array(disp_board, 6)

        self.display_row_indexes()

        for row in disp_board:
            print(row)

    def display_row_indexes(self):
        for i in range(6):
            print(i, end=" ")

        print()

ui = Terminal_UI()
    
ui.display_board()
    

