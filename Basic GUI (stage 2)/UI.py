from Game import Game
from utility_functions import oneD_to_twoD_array
import re
from BoardConstants import BoardConstants
import PySimpleGUI as sg
import textwrap

# ! todo: change uses of class attributes to use self instead of class name


class UI:

    def __init__(self):
        self.__UI_type = None
        self.__game = None
    def get_UI_type(self):

        return self.__UI_type
    
    def play_game(self):
        raise NotImplementedError


class Terminal_UI(UI):
    def __init__(self):
        super().__init__()
        self.__UI_type = "TERMINAL"
    
    def get_UI_type(self):
        return self.__UI_type
    
    def __setup_game(self):
        game = Game(
            player1_name=input("Enter the name of player 1: "),
            player2_name=input("Enter the name of player 2: ")
        )
        return game
    
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

    BUTTON_SIZE = 30
    FONT = "Helvetica"
    TITLE_FONT_SIZE = 25
    BUTTON_DIMENSIONS = (10, 1)
    COLUMN_PAD = 20
    PARAGRAPH_FONT_SIZE = 15

    SUBHEADING_FONT_PARAMS = (FONT, PARAGRAPH_FONT_SIZE, "bold", "underline")
    PARAGRAPH_FONT_PARAMS = (FONT, PARAGRAPH_FONT_SIZE)

    def __init__(self):
        super().__init__()
        self.__UI_type = "GRAPHICAL"

        with open("dummy_text", "r") as f:
            self.__dummy_text = textwrap.fill(f.read(), 140)

        sg.theme('DarkTanBlue')

        self.__current_page = "home_page"
        self.__highlighted_board_positions = []

        self.__window = self.__setup_home_page()


    def __create_window(self, title, layout, justification, transparent=False):
        
        if transparent:
            transparent_colour = sg.theme_background_color()
        else:
            transparent_colour = None

        window = sg.Window(
            title=title,
            layout=layout,
            size=(700, 700),
            resizable=False,
            keep_on_top=True,
            margins=(20,20),
            element_justification=justification,
            # transparent_color=transparent_colour,
            # alpha_channel=0.1,
            text_justification=justification # ! might break things check this
        ).finalize()

        # window.TKroot.attributes("-transparentcolor", "black")

        # sg.LOOK_AND_FEEL_TABLE['Transparent'] = {'BACKGROUND': '#FFFFFF00'}
        # sg.ChangeLookAndFeel('Transparent')


        # full screen without the maximise animtation
        window.TKroot.geometry("{0}x{1}+0+0".format(window.TKroot.winfo_screenwidth(), window.TKroot.winfo_screenheight()))

        self.__window = window
        return window

    def get_UI_type(self):
        return self.__UI_type
    
    def __setup_home_page(self):

        buttons_layout = [
            [sg.Button("New Game", pad=(15, 10), font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="new_game_button")],
            [sg.Button("Help", pad=(15, 10), font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="help_button",)],
            [sg.Button("Exit", pad=(15, 10), font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="exit_button")],
        ]

        buttons_frame = sg.Frame(title="", layout=buttons_layout, border_width=3, pad=(0, self.COLUMN_PAD))

        layout = [
            [self.__create_menu()],
            [sg.Text("Surakarta", pad=(0, self.COLUMN_PAD), font=(self.FONT, self.TITLE_FONT_SIZE))],
            [buttons_frame]
        ]


        return self.__create_window("Surakarta", layout, "center")
    
    def __create_menu(self):

        menu_layout = [
            ["Utilities", ["Home"]],
        ]

        return sg.Menu(menu_layout, pad=(0, self.COLUMN_PAD))
        

    def __setup_new_game_page(self):
        
        
        AI_input_layout = [
            [sg.Text("Difficulty", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [sg.Slider(range=(1, 3), default_value=1, orientation="h", size=(40, 15), pad=(0, self.COLUMN_PAD), key="difficulty_slider")],
            [sg.Text("Player Name", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [sg.InputText("Enter your name", pad=(0, self.COLUMN_PAD), key="player_name_input")],
        ]

        AI_input_frame = sg.Frame(title="", key="AI_play_inputs", layout=AI_input_layout, border_width=0, pad=(0, self.COLUMN_PAD), visible=False)

        Local_input_layout = [
            [sg.Text("Player 1 Name", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [sg.InputText("Enter your name", pad=(0, self.COLUMN_PAD), key="player_1_name_input")],
            [sg.Text("Player 2 Name", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [sg.InputText("Enter your name", pad=(0, self.COLUMN_PAD), key="player_2_name_input")],
        ]

        Local_input_frame = sg.Frame(title="", key="local_play_inputs", layout=Local_input_layout, border_width=0, pad=(0, self.COLUMN_PAD), visible=False)
        
        layout = [
            [self.__create_menu()],
            [sg.Button("Local Play", font=(self.FONT, self.BUTTON_SIZE), pad=(100,100),size=self.BUTTON_DIMENSIONS, key="local_play_button"), sg.Button("AI Play", font=(self.FONT, self.BUTTON_SIZE), pad=(100,100), size=self.BUTTON_DIMENSIONS, key="AI_play_button")],
            [AI_input_frame, Local_input_frame],
            [sg.Button("Submit", font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="submit_local_play_button", visible=False), sg.Button("Submit", font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="submit_AI_play_button", visible=False)],
        ]

        self.__window.close()
        self.__window = self.__create_window("New Game", layout, "center")

    def __setup_help_page(self):

        text_layout = [
            [sg.Text("What is Surakarta?", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [sg.Text(self.__dummy_text, pad=(0, self.COLUMN_PAD), font=self.PARAGRAPH_FONT_PARAMS)],
            [sg.Text("Rules", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [sg.Text(self.__dummy_text, pad=(0, self.COLUMN_PAD), font=self.PARAGRAPH_FONT_PARAMS)],
        ]

        text_frame = sg.Frame(title="", layout=text_layout, border_width=0, pad=(120, self.COLUMN_PAD))


        layout = [
            [self.__create_menu()],
            [text_frame],
            [sg.Image("board_img.png", expand_x=True, expand_y=True)],
        ]

        self.__window.close()

        self.__window = self.__create_window("Help Page", layout, "center")

    def __toggle_play_inputs(self, key_to_make_visible):
        if key_to_make_visible == "AI_play_inputs":
            self.__window["local_play_inputs"].update(visible=False)
            self.__window["AI_play_inputs"].update(visible=True)
            self.__window["submit_AI_play_button"].update(visible=True)
            self.__window["submit_local_play_button"].update(visible=False)
        
        elif key_to_make_visible == "local_play_inputs":
            self.__window["local_play_inputs"].update(visible=True)
            self.__window["AI_play_inputs"].update(visible=False)
            self.__window["submit_AI_play_button"].update(visible=False)
            self.__window["submit_local_play_button"].update(visible=True)

    def __make_piece_button(self, piece_type, key, visible=False):
        return sg.Button("", image_filename=f"{piece_type}_counter.png", visible=visible, pad=(40,40), key=key, button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0)

    def __setup_match_page(self, display_board):

        board_layout = []

        for i, row in enumerate(display_board):
            for j, counter in enumerate(row):
                
                key = f"{i},{j}"

                if counter == None:
                    button = self.__make_piece_button("blank", key, visible=True)

                elif counter == "y":
                    button = self.__make_piece_button("y", key, visible=True)

                elif counter == "g":
                    button = self.__make_piece_button("g", key, visible=True)

                board_layout.append(button)

        board_layout = oneD_to_twoD_array(board_layout, len(display_board))

        player_turn_layout = [
            [sg.Text(f"{self.__game.get_player1_name()}'s Turn", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS, visible=True)],
            [sg.Text(f"{self.__game.get_player2_name()}'s Turn", pad=(0, self.COLUMN_PAD), font=self.PARAGRAPH_FONT_PARAMS, visible=False)],
        ]

        player_turn_frame = sg.Frame("", layout=player_turn_layout, border_width=0)

        move_option = sg.Radio("Move", key="move_type_radio_move", group_id="move_type_radio", font=self.SUBHEADING_FONT_PARAMS)
        capture_option = sg.Radio("Capture", key="move_type_radio_capture", group_id="move_type_radio", font=self.SUBHEADING_FONT_PARAMS)
        submit_move_button = sg.Button("Submit Move", font=(self.FONT, 15), key="submit_move_button")

        layout = [
            [self.__create_menu()],
            [player_turn_frame],
            [move_option, capture_option, submit_move_button],
            [board_layout],
        ]

        self.__create_window("Match", layout, "center")

    def run_gui(self):
        while True:
            event, values = self.__window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break

            if event == "new_game_button":
                self.__setup_new_game_page()                

            elif event == "help_button":
                self.__setup_help_page()

            elif event == "AI_play_button":
                self.__toggle_play_inputs("AI_play_inputs")

            elif event == "local_play_button":
                self.__toggle_play_inputs("local_play_inputs")

            elif event == "submit_local_play_button":
                self.__setup_game(values["player_1_name_input"], values["player_2_name_input"])
                self.play_game()

            elif event == "submit_AI_play_button":
                # print("AI SUBMIT")
                pass

            elif self.__is_board_position(event):
                self.__toggle_highlight_board_position(event)


            elif event == "Home":
                self.__setup_home_page() # ! FIXME doesn't fully work (doesn't close the window)

            elif event == "submit_move_button":

                start_cords = self.__str_key_to_cords_tuple(self.__highlighted_board_positions[0])
                end_cords = self.__str_key_to_cords_tuple(self.__highlighted_board_positions[1])

                start_loc = self.__game.get_board_state()[start_cords[0]][start_cords[1]]
                end_loc = self.__game.get_board_state()[end_cords[0]][end_cords[1]]

                if values["move_type_radio_move"]:
                    move_type = "move"
                
                elif values["move_type_radio_capture"]:
                    move_type = "capture"

                print("CHECKING MOVE LEGALLITY")

                print("move type: ", move_type)

                if self.__game.is_legal_move(start_loc, end_loc, move_type):
                    print("MOVE IS LEGAL")

                    self.__update_board(start_loc, end_loc)
                    self.__game.move_piece(start_loc, end_loc)

                else:
                    print("ILLEGAL MOVE")

                self.__game.switch_current_player()

                # (for loop doesn't work because the list you iterate over gets changed)
                self.__toggle_highlight_board_position(self.__highlighted_board_positions[1])
                self.__toggle_highlight_board_position(self.__highlighted_board_positions[0])


                self.__highlighted_board_positions = []

            
        self.__window.close()


    def __update_board(self, start_loc, end_loc):
    
        start_cords = f"{start_loc.get_cords()[0]},{start_loc.get_cords()[1]}"
        end_cords = f"{end_loc.get_cords()[0]},{end_loc.get_cords()[1]}"

        self.__window[f"{start_cords}"].update(image_filename=f"blank_counter.png")   
        self.__window[f"{end_cords}"].update(image_filename=f"{start_loc.get_colour()}_counter.png") 

        

    def __is_board_position(self, key):
        # if it's a tuple containing two elements where each element is a digit from 0 to 5 inclusive
        # use regex
        pattern = r'^[0-5],[0-5]$'
        if bool(re.match(pattern, key)):
            return True
        
    def __str_key_to_cords_tuple(self, string_key):
        return tuple(int(i) for i in string_key.split(","))
    




    def __toggle_highlight_board_position(self, key):
            
        button = self.__window[key]

        if key not in self.__highlighted_board_positions:
            button.update(button_color=('white', 'pink'))
            self.__highlighted_board_positions.append(key)

        else:
            print("IN THE ELSE")
            button.update(button_color=('white', sg.theme_background_color()))
            self.__highlighted_board_positions.remove(key)        


    def __setup_game(self, name1, name2):
        self.__game = Game(name1, name2)

    def play_game(self):

        # ! CODE THIS
        display_board = [[i.get_colour() for i in row] for row in self.__game.get_board_state()]

        for i in display_board:
            print(i)

        self.__setup_match_page(display_board)


ui = Graphical_UI()

ui.run_gui()