from Game import Game
from utility_functions import oneD_to_twoD_array
import re
from BoardConstants import BoardConstants
import PySimpleGUI as sg

# ! todo: change uses of class attributes to use self instead of class name


class UI:

    def __init__(self):
        self.__UI_type = None
        self.__game = self.__setup_game()

    def get_UI_type(self):
        return self.__UI_type
    
    def __setup_game(self):
        # player1name = input("Enter player 1's name: ")
        # player2name = input("Enter player 2's name: ")
        # TEST CODE
        player1name = "Player 1 (B)"
        player2name = "Player 2 (G)"
        # END TEST CODE
        return Game(player1name, player2name)
    
    def play_game(self):
        raise NotImplementedError


class Terminal_UI(UI):
    def __init__(self):
        super().__init__()
        self.__UI_type = "TERMINAL"
    
    def get_UI_type(self):
        return self.__UI_type
    
    def get_cords_from_user(self, prompt):

        """Gets a valid coordinate from the user in the form 'r,c' where r and c are integers between 0 and 5 inclusive."""

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
                if loc.get_piece() == None:
                    disp_board.append(f"{'.'}")
                else:
                    disp_board.append(loc.get_colour())
        
        disp_board = oneD_to_twoD_array(disp_board, BoardConstants.MAX_ROW_INDEX + 1)

        self.__display_row_indexes()

        for i,row in enumerate(disp_board):
            print(f"{i} | ", end=" ")
            print("  ".join(row))

    def __display_row_indexes(self): # ! MAKE THIS MORE READABLE
        print("     ", end="")
        print("  ".join([str(i) for i in range(6)]))
        print("    ", end="")
        print("—" * 17)

    def display_winner(self):
        winner = self.__game.get_winner()
        if winner == "DRAW":
            print("The game has ended in a draw.")
        else:
            print(f"{winner.get_name()} won!")

    def get_move_type(self):

        """Gets a valid move type from the user. Valid move types are 'move' and 'capture'."""

        valid = False
        while not valid:
            move_type = input("Enter 'move' for an ordinary move to an adjacent position or 'capture' for a capturing move: ")
            if move_type == "move" or move_type == "capture":
                valid = True
            else:
                print("Invalid move type. Please try again.")
        return move_type

    def play_game(self):

        """The main game loop. Runs until the game is over."""

        while not self.__game.get_game_over():
            self.display_board()
            print()
            print(f"{self.__game.get_current_player().get_name()}'s turn.")
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

            if move_type == "move":
                self.__game.move_piece(start_loc, end_loc)

            elif move_type == "capture":
                self.__game.capture_piece(start_loc, end_loc)

            self.__game.switch_current_player()
            self.__game.set_game_status()

        self.display_board()
        self.display_winner()
      




class Graphical_UI(UI):

    BUTTON_SIZE = 15
    FONT = "Helvetica"
    TITLE_FONT_SIZE = 25
    BUTTON_DIMENSIONS = (10, 1)
    COLUMN_PAD = 20

    def __init__(self):
        super().__init__()
        self.__UI_type = "GRAPHICAL"

        sg.theme('DarkTanBlue') 

        self.__home_layout = self.__setup_home_menu()
        self.__new_game_layout = self.__setup_new_game()

        # self.__layout_stack = [self.__home_layout]
        self.__master_layout = [
            [sg.Column(self.__home_layout, key="col1", visible=True)],
            [sg.Column(self.__new_game_layout, key="col2", visible=False)]
        ]

        self.__window = self.__setup_window()

    def get_UI_type(self):
        return self.__UI_type
    
    def __setup_home_menu(self):

        buttons_layout = [
            [sg.Button("New Game", pad=(15, 10), font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="new_game")],
            [sg.Button("Help", pad=(15, 10), font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS)],
            [sg.Button("Exit", pad=(15, 10), font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS)],
        ]

        buttons_frame = sg.Frame(title="", layout=buttons_layout, border_width=3, pad=(0, self.COLUMN_PAD))

        layout = [
            [sg.Titlebar('Surakarta')],
            [sg.Text("Surakarta", pad=(0, self.COLUMN_PAD), font=(self.FONT, self.TITLE_FONT_SIZE))],
            [buttons_frame]
        ]

        return layout
    
    def __setup_new_game(self):
        layout = [sg.Text("new page")]
        return layout

    def __setup_window(self):
        return sg.Window(
            title="Surakarta",
            layout=self.__master_layout,
            size=(700, 700),
            element_justification="center",
        )
    
    def play_game(self):
        while True:
            event, values = self.__window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            
            if event == "new_game":
                print("attempting to change")
                # self.__layout_stack.append(self.__new_game_layout)
                self.__window["col1"].update(visible=False)
                self.__window["col2"].update(visible=True)

        self.__window.close()


ui = Graphical_UI()

ui.play_game()