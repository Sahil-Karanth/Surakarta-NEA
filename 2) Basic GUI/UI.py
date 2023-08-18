from Game import Game
from utility_functions import oneD_to_twoD_array
import re
import sys
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

        self.__highlighted_board_positions = []

        self.__window = None
        self.__setup_home_page()

        self.__game = None

        self.__capture_count_TEST = 0 # ! DELETE ME TEST CODE


    def __create_window(self, title, layout, justification):

        """Creates a window with the given title, layout and justification"""

        self.__window = sg.Window(
            title=title,
            layout=layout,
            size=(700, 700),
            resizable=False,
            keep_on_top=True,
            margins=(20,20),
            element_justification=justification,
            text_justification=justification # ! when writing help page check if I need this
        ).finalize()

        self.__maximise_window()

        return self.__window

    def get_UI_type(self):
        return self.__UI_type
    
    def __maximise_window(self):

        """Maximises the window without an animation"""

        self.__window.TKroot.geometry("{0}x{1}+0+0".format(self.__window.TKroot.winfo_screenwidth(), self.__window.TKroot.winfo_screenheight()))
    
    def __setup_home_page(self):

        """Creates the home page window"""

        button_pad = (15, 10)
        buttons_layout = [
            [sg.Button("New Game", pad=button_pad, font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="new_game_button")],
            [sg.Button("Help", pad=button_pad, font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="help_button",)],
            [sg.Button("Exit", pad=button_pad, font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="exit_button")],
        ]

        buttons_frame = sg.Frame(title="", layout=buttons_layout, border_width=3, pad=(0, self.COLUMN_PAD))

        layout = [
            [self.__create_menu()],
            [sg.Text("Surakarta", pad=(0, self.COLUMN_PAD), font=(self.FONT, self.TITLE_FONT_SIZE))],
            [buttons_frame]
        ]


        # if returning to the home page (self.__window is not None), close the current window
        if self.__window:
            self.__window.close()

        self.__create_window("Surakarta", layout, "center")
    
    def __create_menu(self):

        """Creates the menu which is displayed on every page"""

        menu_layout = [
            ["Utilities", ["Home"]],
        ]

        return sg.Menu(menu_layout, pad=(0, self.COLUMN_PAD))
        

    def __setup_new_game_page(self):
        
        """Creates the new game page window"""
        
        AI_input_layout = [
            [sg.Text("Difficulty", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [sg.Slider(range=(1, 3), default_value=1, orientation="h", size=(40, 15), pad=(0, self.COLUMN_PAD), key="difficulty_slider")],
            [sg.Text("Player Name", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [sg.InputText("Enter your name", pad=(0, self.COLUMN_PAD), key="player_name_input")],
        ]

        AI_input_frame = sg.Frame(title="", key="AI_play_inputs", layout=AI_input_layout, border_width=0, pad=(0, self.COLUMN_PAD), visible=False)

        Local_input_layout = [
            [sg.Text("Player 1 Name", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [sg.InputText("Player 1", pad=(0, self.COLUMN_PAD), key="player_1_name_input")],
            [sg.Text("Player 2 Name", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [sg.InputText("Player 2", pad=(0, self.COLUMN_PAD), key="player_2_name_input")],
        ]

        Local_input_frame = sg.Frame(title="", key="local_play_inputs", layout=Local_input_layout, border_width=0, pad=(0, self.COLUMN_PAD), visible=False)

        layout = [
            [self.__create_menu()],
            [sg.Button("Local Play", font=(self.FONT, self.BUTTON_SIZE),pad=(100,100),size=self.BUTTON_DIMENSIONS, key="local_play_button"), sg.Button("AI Play", font=(self.FONT, self.BUTTON_SIZE), pad=(100,100), size=self.BUTTON_DIMENSIONS, key="AI_play_button")],
            [AI_input_frame, Local_input_frame],
            [sg.Button("Submit", font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="submit_local_play_button", visible=False), sg.Button("Submit", font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="submit_AI_play_button", visible=False)],
        ]

        self.__window.close()
        self.__window = self.__create_window("New Game", layout, "center")

    def __setup_help_page(self):

        """Creates the help page window"""

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

        """Toggles between the AI and local play inputs"""

        # ! haven't grouped the submit buttons into their respective frames because of formatting issues that come with this

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
        return sg.Button("", image_filename=f"{piece_type}_counter.png", visible=visible, pad=(30,30), key=key, button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0)

    def __setup_match_page(self):

        """Creates the match page window where the game is played"""

        display_board = [[i.get_colour() for i in row] for row in self.__game.get_board_state()]
        board_layout = []

        for i, row in enumerate(display_board):
            for j, counter in enumerate(row):
                
                key = f"{i},{j}"

                if counter == None:
                    button = self.__make_piece_button("blank", key, visible=True)

                elif counter == "y":
                    button = self.__make_piece_button(BoardConstants.PLAYER_1_COLOUR, key, visible=True)

                elif counter == "g":
                    button = self.__make_piece_button(BoardConstants.PLAYER_2_COLOUR, key, visible=True)

                board_layout.append(button)

        board_layout = oneD_to_twoD_array(board_layout, len(display_board))

        player_turn_layout = [
            [sg.Text(f"{self.__game.get_player1_name()}'s Turn", key="player1_turn_text", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS, visible=True)],
            [sg.Text(f"{self.__game.get_player2_name()}'s Turn", key="player2_turn_text", pad=(0, self.COLUMN_PAD), font=self.PARAGRAPH_FONT_PARAMS, visible=False)],
        ]

        player_turn_frame = sg.Frame("", layout=player_turn_layout, border_width=0)

        move_option = sg.Radio("Move", key="move_type_radio_move", group_id="move_type_radio", font=self.SUBHEADING_FONT_PARAMS)
        capture_option = sg.Radio("Capture", key="move_type_radio_capture", group_id="move_type_radio", font=self.SUBHEADING_FONT_PARAMS)
        submit_move_button = sg.Button("Submit Move", font=(self.FONT, 15), key="submit_move_button")

        player1_captured = BoardConstants.NUM_STARTING_PIECES_EACH - self.__game.get_player2_piece_count()
        player2_captured = BoardConstants.NUM_STARTING_PIECES_EACH - self.__game.get_player1_piece_count()

        player1_captured_layout = [[sg.Text(f"{self.__game.get_player1_name()} captured pieces: {player1_captured}", key="player1_captured_text", font=self.PARAGRAPH_FONT_PARAMS, pad=(50, 0))]]
        player2_captured_layout = [[sg.Text(f"{self.__game.get_player2_name()} captured pieces: {player2_captured}", key="player2_captured_text", font=self.PARAGRAPH_FONT_PARAMS, pad=(50, 0))]]
        
        layout = [
            [self.__create_menu()],
            [player_turn_frame],
            [move_option, capture_option, submit_move_button],
            [sg.Column(player1_captured_layout), sg.Column(board_layout), sg.Column(player2_captured_layout)],
        ]

        self.__window.close()
        self.__create_window("Match", layout, "center")


    def __update_display_number_captured_pieces(self):
        player1_captured = BoardConstants.NUM_STARTING_PIECES_EACH - self.__game.get_player2_piece_count()
        player2_captured = BoardConstants.NUM_STARTING_PIECES_EACH - self.__game.get_player1_piece_count()

        self.__window["player1_captured_text"].update(f"{self.__game.get_player1_name()} captured pieces: {player1_captured}")
        self.__window["player2_captured_text"].update(f"{self.__game.get_player2_name()} captured pieces: {player2_captured}")





    def __make_move_on_display(self, values):

        """updates the onscreen board and game object board with the move made"""

        start_cords = self.__str_key_to_cords_tuple(self.__highlighted_board_positions[0])
        end_cords = self.__str_key_to_cords_tuple(self.__highlighted_board_positions[1])

        start_loc = self.__game.get_board_state()[start_cords[0]][start_cords[1]]
        end_loc = self.__game.get_board_state()[end_cords[0]][end_cords[1]]

        # start_loc_colour = start_loc.get_colour()

        if values["move_type_radio_move"]:
            move_type = "move"
        
        elif values["move_type_radio_capture"]:
            move_type = "capture"

        else:
            sg.popup("Please select a move type", keep_on_top=True)
            self.__toggle_highlight_board_position(self.__highlighted_board_positions[1])
            self.__toggle_highlight_board_position(self.__highlighted_board_positions[0])
            return

        if self.__game.is_legal_move(start_loc, end_loc, move_type):

            self.__update_board_display(start_loc, end_loc)
            self.__game.move_piece(start_loc, end_loc, move_type)

            self.__update_current_player_display()
            self.__game.switch_current_player()

            if move_type == "capture":
                self.__update_display_number_captured_pieces()
                self.__end_if_game_over()
            
        else:
            sg.popup("ILLEGAL MOVE", keep_on_top=True)

        self.__toggle_highlight_board_position(self.__highlighted_board_positions[1])
        self.__toggle_highlight_board_position(self.__highlighted_board_positions[0])

        self.__highlighted_board_positions = []

        if self.__game.is_game_over():
            self.__setup_home_page()


    def __end_if_game_over(self):

        """uses set_game_status to update the game's status and ends the game with a popup if necessary"""

        self.__game.set_game_status()

        if self.__game.is_game_over():
            winning_player = self.__game.get_winner()
            sg.popup(f"{winning_player.get_name()} has won the game!", keep_on_top=True)



    def __update_board_display(self, start_loc, end_loc):

        """updates the onscreen board with the move made"""
    
        start_cords = f"{start_loc.get_cords()[0]},{start_loc.get_cords()[1]}"
        end_cords = f"{end_loc.get_cords()[0]},{end_loc.get_cords()[1]}"

        self.__window[f"{start_cords}"].update(image_filename=f"blank_counter.png")   
        self.__window[f"{end_cords}"].update(image_filename=f"{start_loc.get_colour()}_counter.png") 


    def __update_current_player_display(self):

        """updates the onscreen current player display"""

        current_text = self.__window["player1_turn_text"]

        if self.__game.get_current_player_name() == self.__game.get_player1_name():
            current_text.update(f"{self.__game.get_player2_name()}'s Turn")
        
        elif self.__game.get_current_player_name() == self.__game.get_player2_name():
            current_text.update(f"{self.__game.get_player1_name()}'s Turn")


    def __is_board_position(self, key):

        """checks if the key of a GUI element i a board position meaning it is a tuple containing two elements where each element is a digit from 0 to 5 inclusive""" 

        pattern = r'^[0-5],[0-5]$'
        if bool(re.match(pattern, key)):
            return True
        
    def __str_key_to_cords_tuple(self, string_key):

        """converts a string key of a GUI element in the form 'x,y' to a tuple of the form (x,y) where x and y are integers"""

        return tuple(int(i) for i in string_key.split(","))
    

    def __toggle_highlight_board_position(self, key):

        """toggles the background colour of a board position between white and pink.
        No more than two board positions can be highlighted at once."""
            
        button = self.__window[key]

        if key in self.__highlighted_board_positions:
            button.update(button_color=('pink', sg.theme_background_color()))
            self.__highlighted_board_positions.remove(key)

        elif key not in self.__highlighted_board_positions and len(self.__highlighted_board_positions) < 2:
            button.update(button_color=(sg.theme_background_color(), 'pink'))
            self.__highlighted_board_positions.append(key)


    def __create_game_object(self, name1, name2):
        self.__game = Game(name1, name2)


    def play_game(self):
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
                self.__create_game_object(values["player_1_name_input"], values["player_2_name_input"])
                self.__setup_match_page()

            elif event == "submit_AI_play_button":
                # print("AI SUBMIT")
                pass

            elif self.__is_board_position(event):
                self.__toggle_highlight_board_position(event)

            elif event == "Home":
                self.__window.close()
                self.__setup_home_page()

            elif event == "submit_move_button":
                self.__make_move_on_display(values)

        self.__window.close()