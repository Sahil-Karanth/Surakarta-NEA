from Game import Game
from utility_functions import oneD_to_twoD_array
import re
from BoardConstants import BoardConstants
import PySimpleGUI as sg
import textwrap
import time
from PIL import ImageTk, Image

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
    TITLE_FONT_SIZE = 40
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
        self.__display_board_window = None

        self.__current_page = None
        self.__setup_home_page()

        self.__game = None

        self.__ai_mode = False

        self.capture_count_test = 0


    def __create_window(self, title, layout, justification, maximise=True, size=(700, 700), modal=False, disable_close=False):

        """Creates a window with the given title, layout and justification"""

        window = sg.Window(
            title=title,
            layout=layout,
            size=size,
            resizable=False,
            keep_on_top=True,
            modal=modal,
            disable_close=disable_close,
            # margins=(20,20),
            element_justification=justification,
            text_justification=justification # ! when writing help page check if I need this
        ).finalize()

        if maximise:
            self.__maximise_window(window)

        return window

    def get_UI_type(self):
        return self.__UI_type
    
    def __maximise_window(self, window):

        """Maximises the window without an animation"""

        window.TKroot.geometry("{0}x{1}+0+0".format(window.TKroot.winfo_screenwidth(), window.TKroot.winfo_screenheight()))
    
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

        self.__current_page = "home_page"

        self.__window = self.__create_window("Surakarta", layout, "center")
    
    def __create_menu(self):

        """Creates the menu which is displayed on every page"""

        menu_layout = [
            ["Utilities", ["Home", "Restart Match", "Quit"]],
        ]

        return sg.Menu(menu_layout, pad=(0, self.COLUMN_PAD))
        

    def __setup_new_game_page(self):
        
        """Creates the new game page window"""
        
        AI_input_layout = [
            [sg.Text("Difficulty", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [sg.Slider(range=(1, 3), default_value=1, orientation="h", size=(40, 15), pad=(0, self.COLUMN_PAD), key="difficulty_slider")],
            [sg.Text("Player Name", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [sg.InputText("Player 1", pad=(0, self.COLUMN_PAD), key="player_name_input")],
        ]

        AI_input_col = sg.Column(key="AI_play_inputs", layout=AI_input_layout, pad=(0, self.COLUMN_PAD), visible=False)

        Local_input_layout = [
            [sg.Text("Player 1 Name", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [sg.InputText("Player 1", pad=(0, self.COLUMN_PAD), key="player_1_name_input")],
            [sg.Text("Player 2 Name", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [sg.InputText("Player 2", pad=(0, self.COLUMN_PAD), key="player_2_name_input")],
        ]

        Local_input_col = sg.Column(key="local_play_inputs", layout=Local_input_layout, pad=(0, self.COLUMN_PAD), visible=False)

        layout = [
            [self.__create_menu()],
            [sg.Button("Local Play", font=(self.FONT, self.BUTTON_SIZE),pad=(100,100),size=self.BUTTON_DIMENSIONS, key="local_play_button"), sg.Button("AI Play", font=(self.FONT, self.BUTTON_SIZE), pad=(100,100), size=self.BUTTON_DIMENSIONS, key="AI_play_button")],
            [AI_input_col, Local_input_col],
            [sg.Button("Submit", font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="submit_local_play_button", visible=False), sg.Button("Submit", font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="submit_AI_play_button", visible=False)],
        ]

        self.__window.close()
        self.__current_page = "new_game_page"
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
        self.__current_page = "help_page"
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
        return sg.Button("", image_filename=f"{piece_type}_counter.png", pad=(30,30), visible=visible, key=key, button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0)

    def __make_display_board_window(self):

        layout = [
            [sg.Button("close", key="close_display_board_button")],
            [sg.Canvas(size=(500, 500), key='-CANVAS-')],
        ]

        display_board_window = self.__create_window("Display Board", layout, "center", size=(300, 300), maximise=False, modal=True, disable_close=True)
        # self.__display_board_window = sg.Window('Circle Drawing', layout, keep_on_top=True, finalize=True)

        canvas = display_board_window['-CANVAS-'].TKCanvas
        image_path = 'blank_board.png'
        image = Image.open(image_path)
        image.thumbnail((300, 300))  # Resize the image to fit the canvas
        background_img = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, image=background_img, anchor='nw')


        while True:
            event, values = display_board_window.read()
            if event == "close_display_board_button":
                break

        display_board_window.close()


    def __setup_match_page(self, player1name, player2name, ai_level=None):

        """Creates the match page window where the game is played"""

        self.__create_game_object(player1name, player2name, ai_level)

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
            [sg.Text(f"{self.__game.get_player_name(1)}'s Turn", key="player1_turn_text", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS, visible=True)],
            [sg.Text(f"{self.__game.get_player_name(2)}'s Turn", key="player2_turn_text", pad=(0, self.COLUMN_PAD), font=self.PARAGRAPH_FONT_PARAMS, visible=False)],
        ]

        player_turn_frame = sg.Frame("", layout=player_turn_layout, border_width=0)

        move_option = sg.Radio("Move", key="move_type_radio_move", group_id="move_type_radio", font=self.SUBHEADING_FONT_PARAMS)
        capture_option = sg.Radio("Capture", key="move_type_radio_capture", group_id="move_type_radio", font=self.SUBHEADING_FONT_PARAMS)
        submit_move_button = sg.Button("Submit Move", font=(self.FONT, 15), key="submit_move_button")

        undo_move_button = sg.Button("Undo Move", font=(self.FONT, 15), key="undo_move_button")

        player1_captured = BoardConstants.NUM_STARTING_PIECES_EACH - self.__game.get_player_piece_count(2)
        player2_captured = BoardConstants.NUM_STARTING_PIECES_EACH - self.__game.get_player_piece_count(1)

        player1_captured_layout = [[sg.Text(f"{self.__game.get_player_name(1)} captured pieces: {player1_captured}", key="player1_captured_text", font=self.PARAGRAPH_FONT_PARAMS, pad=(50, 0))]]
        player2_captured_layout = [[sg.Text(f"{self.__game.get_player_name(2)} captured pieces: {player2_captured}", key="player2_captured_text", font=self.PARAGRAPH_FONT_PARAMS, pad=(50, 0))]]
        
        layout = [
            [self.__create_menu()],
            [sg.Button("show board", key="show_board_button")], # ! TESTING
            [player_turn_frame],
            [undo_move_button, move_option, capture_option, submit_move_button],
            [sg.Column(player1_captured_layout), sg.Column(board_layout), sg.Column(player2_captured_layout)],
        ]

        self.__window.close()
        self.__current_page = "match_page"
        self.__window = self.__create_window("Match", layout, "center")

        # self.__make_display_board_window()


    def __update_display_number_captured_pieces(self):
        player1_captured = BoardConstants.NUM_STARTING_PIECES_EACH - self.__game.get_player_piece_count(2)
        player2_captured = BoardConstants.NUM_STARTING_PIECES_EACH - self.__game.get_player_piece_count(1)

        self.__window["player1_captured_text"].update(f"{self.__game.get_player_name(1)} captured pieces: {player1_captured}")
        self.__window["player2_captured_text"].update(f"{self.__game.get_player_name(2)} captured pieces: {player2_captured}")


    def __update_game_and_UI_post_move(self, start_loc, end_loc, move_type):

        move_obj = self.__game.move_piece(start_loc, end_loc, move_type)
        self.__update_board_display(move_obj.get_start_cords(), move_obj.get_end_cords(), move_obj.get_start_colour())

        # for row in self.__game.get_board_state():
        #     print([i.get_colour() for i in row])

        self.__update_current_player_display()
        self.__game.switch_current_player()



    def __make_move_on_display(self, values, ai_mode=False):

        """updates the onscreen board and game object board with the move made"""

        start_cords = self.__str_key_to_cords_tuple(self.__highlighted_board_positions[0])
        end_cords = self.__str_key_to_cords_tuple(self.__highlighted_board_positions[1])

        start_loc = self.__game.get_board_state()[start_cords[0]][start_cords[1]]
        end_loc = self.__game.get_board_state()[end_cords[0]][end_cords[1]]

        if values["move_type_radio_move"]:
            move_type = "move"
        
        elif values["move_type_radio_capture"]:
            move_type = "capture"

        else:
            sg.popup("Please select a move type", keep_on_top=True)
            self.__toggle_highlight_board_position(self.__highlighted_board_positions[1])
            self.__toggle_highlight_board_position(self.__highlighted_board_positions[0])
            return
        
        prev_move_legal = True

        if self.__game.is_legal_move(start_loc, end_loc, move_type):

            self.__update_game_and_UI_post_move(start_loc, end_loc, move_type)

            if move_type == "capture":
                self.capture_count_test += 1
                self.__update_display_number_captured_pieces()
                self.__end_if_game_over()
            
        else:
            sg.popup("ILLEGAL MOVE", keep_on_top=True)
            prev_move_legal = False

        self.__toggle_highlight_board_position(self.__highlighted_board_positions[1])
        self.__toggle_highlight_board_position(self.__highlighted_board_positions[0])

        self.__highlighted_board_positions = []

        if self.__game.is_game_over():
            self.__setup_home_page()


        if ai_mode and prev_move_legal:
            move = self.__game.get_ai_move()

            time.sleep(0.1) # delay so the move is not made instantly which is jarring

            self.__update_game_and_UI_post_move(move.get_start_loc(), move.get_end_loc(), move.get_move_type())

            if move.get_move_type() == "capture":
                self.__update_display_number_captured_pieces()
                self.__end_if_game_over()


    def __end_if_game_over(self):

        """uses set_game_status to update the game's status and ends the game with a popup if necessary"""

        self.__game.set_game_status()

        if self.__game.is_game_over():
            winning_player = self.__game.get_winner()
            sg.popup(f"{winning_player.get_name()} has won the game!", title="Game Over", keep_on_top=True)
            self.__setup_home_page()
  
    def __update_board_display(self, start_cords, end_cords, start_colour):

        """updates the onscreen board with the move made. undo is True when undoing a move"""
    
        start_cords_str = f"{start_cords[0]},{start_cords[1]}"
        end_cords_str = f"{end_cords[0]},{end_cords[1]}"

        self.__window[f"{start_cords_str}"].update(image_filename=f"blank_counter.png")   

        self.__window[f"{end_cords_str}"].update(image_filename=f"{start_colour}_counter.png")

    def __update_current_player_display(self):

        """updates the onscreen current player display"""

        current_text = self.__window["player1_turn_text"]

        if self.__game.get_current_player_name() == self.__game.get_player_name(1):
            current_text.update(f"{self.__game.get_player_name(2)}'s Turn")
        
        elif self.__game.get_current_player_name() == self.__game.get_player_name(2):
            current_text.update(f"{self.__game.get_player_name(1)}'s Turn")


    def __is_board_position(self, key):

        """checks if the key of a GUI element i a board position meaning it is a tuple containing two elements where each element is a digit from 0 to 5 inclusive""" 

        if not key: # makes sure a key of None doesn't cause an error
            return False

        pattern = r'^[0-5],[0-5]$'
        if bool(re.match(pattern, key)):
            return True
        
    def __str_key_to_cords_tuple(self, string_key):

        """converts a string key of a GUI element in the form 'x,y' to a tuple of the form (x,y) where x and y are integers"""

        return tuple(int(i) for i in string_key.split(","))
    
    def __tuple_key_cords_str(self, tuple_key):

        """converts a tuple key of the form (x,y) to a string of the form 'x,y' where x and y are integers"""

        return f"{tuple_key[0]},{tuple_key[1]}"
    

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


    def __undo_move(self, ai_mode=False):

        """undoes the last move made. If in AI mode, undoes two moves"""

        move_obj = self.__game.undo_move()

        if move_obj == None:
            sg.popup("No moves to undo", keep_on_top=True)
            return
        
        self.__update_board_display(move_obj.get_end_cords(), move_obj.get_start_cords(), move_obj.get_start_colour())

        if move_obj.get_move_type() == "capture":            
            cords = self.__tuple_key_cords_str(move_obj.get_end_loc().get_cords())
            self.__window[f"{cords}"].update(image_filename=f"{move_obj.get_end_colour()}_counter.png")


        self.__update_display_number_captured_pieces()
        self.__update_current_player_display()
        self.__game.switch_current_player()

        if ai_mode:
            self.__undo_move()


    def __difficulty_level_to_ai_name(self, difficulty_level):
        name_level_dict = {
            1: "Easy AI",
            2: "Medium AI",
            3: "Hard AI"
        }

        return name_level_dict[difficulty_level]

    def __create_game_object(self, name1, name2, ai_level):
        self.__game = Game(name1, name2, ai_level=ai_level)

    def play_game(self):

        while True:
            event, values = self.__window.read()

            if event == sg.WIN_CLOSED or event == 'Quit':
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
                self.__setup_match_page(values["player_1_name_input"], values["player_2_name_input"])

            elif event == "submit_AI_play_button":
                difficulty_level = int(values['difficulty_slider'])
                ai_name = self.__difficulty_level_to_ai_name(difficulty_level)
                self.__ai_mode = True
                self.__setup_match_page(values["player_1_name_input"], ai_name, ai_level=difficulty_level)

            elif event == "show_board_button":
                self.__make_display_board_window()

            elif event == "undo_move_button":
                self.__undo_move(self.__ai_mode)

            elif self.__is_board_position(event):
                self.__toggle_highlight_board_position(event)

            elif event == "Home":
                self.__window.close()
                self.__setup_home_page()

            elif event == "Restart Match":
                if self.__current_page == "match_page":
                    player1_name = self.__game.get_player_name(1)
                    player2_name = self.__game.get_player_name(2)
                    self.__setup_match_page(player1_name, player2_name)

                else:
                    sg.popup("You can only restart a match from the match page", title="Error Restarting Match", keep_on_top=True)


            elif event == "submit_move_button":
                self.__make_move_on_display(values, self.__ai_mode)

        self.__window.close()