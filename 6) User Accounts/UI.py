from Game import Game
from utility_functions import oneD_to_twoD_array, create_circle
import re
from BoardConstants import BoardConstants
import PySimpleGUI as sg
import textwrap
import time
from PIL import ImageTk, Image
from Database import Database
import datetime


# ! todo: change uses of class attributes to use self instead of class name
# ! todo: add validation for all ways a user could make the game crash
# ! todo: reject usernames or entered names that are the AI names
# ! todo: make sure the user can't spawn a bunch of display board windows
# ! todo: FIX LOOP UPDATES when a game is loaded


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
    TITLE_FONT_SIZE = 60
    BUTTON_DIMENSIONS = (10, 1)
    COLUMN_PAD = 20
    LOGIN_PAD = 10
    PARAGRAPH_FONT_SIZE = 15

    SUBHEADING_FONT_PARAMS = (FONT, PARAGRAPH_FONT_SIZE, "bold")
    PARAGRAPH_FONT_PARAMS = (FONT, PARAGRAPH_FONT_SIZE)

    DISP_BOARD_PIECE_SPACING = 43
    DISP_BOARD_INITAL_X = 128
    DISP_BOARD_INITAL_Y = 109
    DISP_BOARD_PIECE_RADIUS = 15

    AVAILABLE_PIECE_COLOURS = ["yellow", "green", "red", "lightblue", "orange", "black"]


    def __init__(self):
        super().__init__()
        self.__UI_type = "GRAPHICAL"

        with open("dummy_text", "r") as f:
            self.__dummy_text = textwrap.fill(f.read(), 140)

        # sg.theme('DarkTeal10')
        sg.theme('Dark')

        self.__highlighted_board_positions = []

        self.__main_window = None
        self.__display_board_window = None
        self.__login_window = None

        self.__logged_in = False
        self.__logged_in_username = None 
        self.__preferred_piece_colour = None

        self.__current_page = None
        self.__setup_home_page()

        self.__game = None
        self.__game_is_loaded = False
        self.__ai_mode = False
        self.__ai_name = None

        self.__db = Database("database.db")

        self.capture_count_test = 0

        self.__ai_name_to_level_num_map = {
            1: "Easy AI",
            2: "Medium AI",
            3: "Hard AI"
        }

        self.__ai_level_num_to_name_map = {
            "Easy AI": 1,
            "Medium AI": 2,
            "Hard AI": 3
        }


    def __create_window(self, title, layout, justification, maximise=True, size=(700, 700), modal=False, disable_close=False, keep_on_top=False):

        """Creates a window with the given title, layout and justification"""

        window = sg.Window(
            title=title,
            layout=layout,
            size=size,
            resizable=False,
            keep_on_top=keep_on_top,
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

        new_game_button = sg.Button("New Game", pad=button_pad, font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="new_game_button")
        load_game_button = sg.Button("Load Game", pad=button_pad, font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="load_game_button")
        show_stats_button = sg.Button("Show Stats", pad=button_pad, font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="show_stats_button")
        login_button = sg.Button("Login", pad=button_pad, font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="login_button")
        signup_button = sg.Button("Sign Up", pad=button_pad, font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="signup_button")
        help_button = sg.Button("Help", pad=button_pad, font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="help_button")

        buttons_layout = [
            [new_game_button, login_button],
            [load_game_button, signup_button],
            [show_stats_button, help_button],
        ]

        buttons_frame = sg.Frame(title="", layout=buttons_layout, border_width=3, pad=(0, self.COLUMN_PAD))

        layout = [
            [self.__create_menu()],
            [sg.Text("Surakarta", pad=(0, self.COLUMN_PAD), font=(self.FONT, self.TITLE_FONT_SIZE))],
            [buttons_frame]
        ]


        # if returning to the home page (self.__main_window is not None), close the current window
        if self.__main_window:
            self.__main_window.close()

        self.__current_page = "home_page"

        self.__main_window = self.__create_window("Surakarta", layout, "center")
    
    def __create_menu(self):

        """Creates the menu which is displayed on every page"""

        menu_layout = [
            ["Utilities", ["Home", "Show Login Status", "Quit"]],
            ["Match Options", ["Restart Match", "Save Game"]]
        ]

        return sg.Menu(menu_layout, pad=(0, self.COLUMN_PAD))
        

    def __make_login_or_signup_window(self, login_or_signup):
            
            if login_or_signup not in ["login", "signup"]:
                raise ValueError("login_or_signup parameter of the __make_login_or_signup_window method must be either 'login' or 'signup'")
                
            drop_down_menu_layout = []
            modal_height = 270

            if login_or_signup == "signup":
                drop_down_menu_layout = [
                    [sg.Text("Preferred Piece Colour", pad=(0, self.LOGIN_PAD), font=self.PARAGRAPH_FONT_PARAMS)],
                    [sg.Combo(self.AVAILABLE_PIECE_COLOURS, font=self.PARAGRAPH_FONT_PARAMS, expand_x=True, enable_events=True,  readonly=True, key="piece_colour_choice")]
                ]

                modal_height = 350
            
            layout = [
                [sg.Text("Username", pad=(0, self.LOGIN_PAD), font=self.PARAGRAPH_FONT_PARAMS)],
                [sg.InputText("", pad=(0, self.LOGIN_PAD), key=f"{login_or_signup}_username_input", font=self.PARAGRAPH_FONT_PARAMS)],
                [sg.Text("Password", pad=(0, self.LOGIN_PAD), font=self.PARAGRAPH_FONT_PARAMS)],
                [sg.InputText("", pad=(0, self.LOGIN_PAD), key=f"{login_or_signup}_password_input", password_char="*", font=self.PARAGRAPH_FONT_PARAMS)],
                [drop_down_menu_layout],
                [sg.Button("Submit", pad=(0, self.COLUMN_PAD), font=(self.FONT, 15), size=self.BUTTON_DIMENSIONS, key=f"{login_or_signup}_submit_button")]
            ]


            return self.__create_window(login_or_signup.title(), layout, "center", modal=True, keep_on_top=True, size=(300, modal_height), maximise=False, disable_close=False)

    def __get_text_and_input_layout(self, disp_text, inp_default_text, inp_key):

        layout = [
            [sg.Text(disp_text, pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [sg.InputText(inp_default_text, pad=(0, self.COLUMN_PAD), key=inp_key, font=self.PARAGRAPH_FONT_PARAMS)],
        ]

        return layout


    def __setup_new_game_page(self):
        
        """Creates the new game page window"""
        
        player_1_input_visible = not self.__logged_in

        player_1_input_ai_layout = self.__get_text_and_input_layout("Player 1 Name", "Player 1", "player_1_ai_input")
        player_1_ai_input_col = sg.Column(player_1_input_ai_layout, visible=player_1_input_visible)


        AI_input_layout = [
            [sg.Text("Difficulty", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [sg.Slider(range=(1, 3), default_value=1, orientation="h", size=(40, 15), pad=(0, self.COLUMN_PAD), key="difficulty_slider")],
            [player_1_ai_input_col],
        ]

        AI_input_col = sg.Column(key="AI_play_inputs", layout=AI_input_layout, pad=(0, self.COLUMN_PAD), visible=False)

        player_1_input_local_layout = self.__get_text_and_input_layout("Player 1 Name", "Player 1", "player_1_local_input")
        player_1_local_input_col = sg.Column(player_1_input_local_layout, visible=player_1_input_visible)

        Local_input_layout = [
            [player_1_local_input_col],
            [sg.Text("Player 2 Name", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [sg.InputText("Player 2", pad=(0, self.COLUMN_PAD), key="player_2_local_input", font=self.PARAGRAPH_FONT_PARAMS)],
        ]

        Local_input_col = sg.Column(key="local_play_inputs", layout=Local_input_layout, pad=(0, self.COLUMN_PAD), visible=False)

        layout = [
            [self.__create_menu()],
            [sg.Button("Local Play", font=(self.FONT, self.BUTTON_SIZE),pad=(100,100),size=self.BUTTON_DIMENSIONS, key="local_play_button"), sg.Button("AI Play", font=(self.FONT, self.BUTTON_SIZE), pad=(100,100), size=self.BUTTON_DIMENSIONS, key="AI_play_button")],
            [AI_input_col, Local_input_col],
            [sg.Button("Submit", font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="submit_local_play_button", visible=False), sg.Button("Submit", font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="submit_AI_play_button", visible=False)],
        ]

        self.__main_window.close()
        self.__current_page = "new_game_page"
        self.__main_window = self.__create_window("New Game", layout, "center")

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

        self.__main_window.close()
        self.__current_page = "help_page"
        self.__main_window = self.__create_window("Help Page", layout, "center")

    def __toggle_play_inputs(self, key_to_make_visible):

        """Toggles between the AI and local play inputs"""

        # ! haven't grouped the submit buttons into their respective frames because of formatting issues that come with this

        if key_to_make_visible == "AI_play_inputs":
            self.__main_window["local_play_inputs"].update(visible=False)
            self.__main_window["AI_play_inputs"].update(visible=True)
            self.__main_window["submit_AI_play_button"].update(visible=True)
            self.__main_window["submit_local_play_button"].update(visible=False)
        
        elif key_to_make_visible == "local_play_inputs":
            self.__main_window["local_play_inputs"].update(visible=True)
            self.__main_window["AI_play_inputs"].update(visible=False)
            self.__main_window["submit_AI_play_button"].update(visible=False)
            self.__main_window["submit_local_play_button"].update(visible=True)

    def __make_piece_button(self, piece_type, key, visible=False):
        return sg.Button("", image_filename=f"{piece_type}_counter.png", pad=(30,30), visible=visible, key=key, button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0)


    def __draw_pieces_on_disp_board(self, window):

        canvas = window['-CANVAS-'].TKCanvas

        canvas.delete("counter")

        display_board = [[i.get_colour() for i in row] for row in self.__game.get_board_state()]

        for i, row in enumerate(display_board):

            for j, counter in enumerate(row):

                if counter == None:
                    continue
                
                else:
                    create_circle(canvas, self.DISP_BOARD_INITAL_X + (self.DISP_BOARD_PIECE_SPACING * j), self.DISP_BOARD_INITAL_Y + (self.DISP_BOARD_PIECE_SPACING * i), self.DISP_BOARD_PIECE_RADIUS, counter)



    def __make_display_board_window(self):

        layout = [
            [sg.Canvas(size=(500, 500), key='-CANVAS-')],
        ]

        display_board_window = self.__create_window("Display Board", layout, "center", size=(500, 500), maximise=False, modal=False, disable_close=False, keep_on_top=True)

        return display_board_window

    
    def __make_stats_window(self, username):

        ai_match_stats = self.__db.get_user_stats(username)
        ai_stats_table_headers = ["AI Difficulty", "Wins", "Losses"]
        ai_stats_rows = [[element for element in row] for row in ai_match_stats]

        ai_stats_table = sg.Table(ai_stats_rows, ai_stats_table_headers, expand_x=True, background_color="light gray", text_color="black")

        game_history = self.__db.get_game_history(username)
        game_history_table_headers = ["Game Number", "Date", "Opponent", "Winner"]
        game_history_rows = [[element for element in row] for row in game_history]

        game_history_table = sg.Table(game_history_rows, game_history_table_headers, expand_x=True, background_color="light gray", text_color="black")

        layout = [
            [ai_stats_table],
            [game_history_table],
        ]

        stats_window = self.__create_window("Stats", layout, "center", size=(500, 500), maximise=False, modal=False, disable_close=False, keep_on_top=True)

        return stats_window


    def __setup_match_page(self, player1name, player2name, ai_level=None, game_state_string=None, player2_starts=False, player1_num_pieces=BoardConstants.NUM_STARTING_PIECES_EACH, player2_num_pieces=BoardConstants.NUM_STARTING_PIECES_EACH):

        """Creates the match page window where the game is played"""

        self.__create_game_object(player1name, player2name, ai_level, game_state_string, player2_starts, player1_num_pieces, player2_num_pieces)

        if game_state_string:
            self.__game_is_loaded = True

        display_board = [[i.get_colour() for i in row] for row in self.__game.get_board_state()] # ! change name now that I have an actual display board
        board_layout = []

        for i, row in enumerate(display_board):
            for j, counter in enumerate(row):
                
                key = f"{i},{j}"

                if counter == None:
                    button = self.__make_piece_button("blank", key, visible=True)

                else:
                    button = self.__make_piece_button(counter, key, visible=True)

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

        show_display_board_button = sg.Button("show board", key="show_board_button", font=(self.FONT, 15))

        player1_captured = BoardConstants.NUM_STARTING_PIECES_EACH - self.__game.get_player_piece_count(2)
        player2_captured = BoardConstants.NUM_STARTING_PIECES_EACH - self.__game.get_player_piece_count(1)

        player1_captured_layout = [[sg.Text(f"{self.__game.get_player_name(1)} captured pieces: {player1_captured}", key="player1_captured_text", font=self.PARAGRAPH_FONT_PARAMS, pad=(50, 0))]]
        player2_captured_layout = [[sg.Text(f"{self.__game.get_player_name(2)} captured pieces: {player2_captured}", key="player2_captured_text", font=self.PARAGRAPH_FONT_PARAMS, pad=(50, 0))]]
        
        layout = [
            [self.__create_menu()],
            [player_turn_frame],
            [show_display_board_button],
            [undo_move_button, move_option, capture_option, submit_move_button],
            [sg.Column(player1_captured_layout), sg.Column(board_layout), sg.Column(player2_captured_layout)],
        ]

        self.__main_window.close()
        self.__current_page = "match_page"
        self.__main_window = self.__create_window("Match", layout, "center")

        if player2_starts:
            self.__update_current_player_display(self.__game_is_loaded)
            self.__update_display_number_captured_pieces()


    def __update_display_number_captured_pieces(self):
        player1_captured = BoardConstants.NUM_STARTING_PIECES_EACH - self.__game.get_player_piece_count(2)
        player2_captured = BoardConstants.NUM_STARTING_PIECES_EACH - self.__game.get_player_piece_count(1)

        self.__main_window["player1_captured_text"].update(f"{self.__game.get_player_name(1)} captured pieces: {player1_captured}")
        self.__main_window["player2_captured_text"].update(f"{self.__game.get_player_name(2)} captured pieces: {player2_captured}")


    def __update_game_and_UI_post_move(self, start_loc, end_loc, move_type):

        move_obj = self.__game.move_piece(start_loc, end_loc, move_type)
        self.__update_board_display(move_obj.get_start_cords(), move_obj.get_end_cords(), move_obj.get_start_colour())

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
                return
            
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

    def __reset_game_variables(self):

        """resets all game variables to their initial values"""

        self.__game = None
        self.__game_is_loaded = False
        self.__ai_mode = False
        self.__ai_name = None
        self.__highlighted_board_positions = []


    def __end_if_game_over(self):

        """uses set_game_status to update the game's status and ends the game with a popup if necessary"""

        self.__game.set_game_status()

        if self.__game.is_game_over():
            winning_player = self.__game.get_winner()

            sg.popup(f"{winning_player.get_name()} has won the game!", title="Game Over", keep_on_top=True)

            if self.__logged_in and self.__ai_mode:

                human_won = False

                if winning_player.get_name() == self.__logged_in_username:
                    human_won = True

                self.__db.update_user_stats(self.__logged_in_username, human_won, self.__ai_name)

            if self.__game_is_loaded:
                self.__db.delete_saved_game(self.__logged_in_username)


            # add game to game history

            self.__db.add_game_to_history(self.__logged_in_username, self.__game.get_player_name(2), self.__game.get_winner().get_name())

            self.__reset_game_variables()
            self.__setup_home_page()
  
    def __update_board_display(self, start_cords, end_cords, start_colour):

        """updates the onscreen board with the move made. undo is True when undoing a move"""
    
        start_cords_str = f"{start_cords[0]},{start_cords[1]}"
        end_cords_str = f"{end_cords[0]},{end_cords[1]}"

        self.__main_window[f"{start_cords_str}"].update(image_filename=f"blank_counter.png")   

        self.__main_window[f"{end_cords_str}"].update(image_filename=f"{start_colour}_counter.png")

    def __update_current_player_display(self, game_is_loaded=False):

        """updates the onscreen current player display"""

        current_text = self.__main_window["player1_turn_text"]

        # switches the current player display to player 2's name if the game is loaded and it is player 2's turn immediately
        # parameter game_is_loaded is used to prevent this from happening every turn
        if game_is_loaded and self.__game.get_current_player_name() == self.__game.get_player_name(2):
            current_text.update(f"{self.__game.get_player_name(2)}'s Turn")
            return

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
    
    def __get_player1_name(self):

        if self.__logged_in:
            return self.__logged_in_username
        
        else:
            return self.__main_window["player_1_local_input"].get()
    

    def __toggle_highlight_board_position(self, key):

        """toggles the background colour of a board position between white and pink.
        No more than two board positions can be highlighted at once."""
            
        button = self.__main_window[key]

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
            self.__main_window[f"{cords}"].update(image_filename=f"{move_obj.get_end_colour()}_counter.png")


        self.__update_display_number_captured_pieces()
        self.__update_current_player_display()
        self.__game.switch_current_player()

        if ai_mode:
            self.__undo_move()


    def __difficulty_level_to_ai_name(self, difficulty_level):
        return self.__ai_name_to_level_num_map[difficulty_level]

    def __create_game_object(self, name1, name2, ai_level, game_state_string, player2_starts, player1pieces, player2pieces):
        self.__game = Game(name1, name2, ai_level=ai_level, game_state_string=game_state_string, player2_starts=player2_starts, player1_num_pieces=player1pieces, player2_num_pieces=player2pieces)


    def play_game(self):

        disp_win_open = False

        while True:
            window, event, values = sg.read_all_windows()

            if event == sg.WIN_CLOSED or event == 'Quit':
                if window == self.__display_board_window:
                    disp_win_open = False
                    self.__display_board_window.close()

                elif window == self.__main_window:
                    window.close()
                    break

                else:
                    window.close()

            if event == "new_game_button":
                self.__setup_new_game_page()                

            elif event == "help_button":
                self.__setup_help_page()

            elif event == "show_stats_button":
                if self.__logged_in_username:
                    self.__make_stats_window(self.__logged_in_username)

                else:
                    sg.popup("You must be logged in to view your stats", title="Error Showing Stats", keep_on_top=True)
                    

            elif event == "Save Game":
                if self.__current_page == "match_page" and self.__logged_in:

                    if self.__db.game_already_saved(self.__logged_in_username):
                        overwrite = sg.popup_yes_no("You already have a saved game. Do you want to overwrite it?", title="Game Already Saved", keep_on_top=True)
                    
                        if overwrite == "No":
                            continue

                    game_state_string = self.__game.get_game_state_string()
                    player2_starts = self.__game.get_player_name(2) == self.__game.get_current_player_name()

                    self.__db.save_game_state(self.__logged_in_username, game_state_string, self.__game.get_player_name(2), player2_starts, self.__game.get_player_piece_count(1), self.__game.get_player_piece_count(2))
                    sg.popup("Game saved", title="Game Saved", keep_on_top=True)

                else:
                    sg.popup("You can only save a game from the match page", title="Error Saving Game", keep_on_top=True)

            elif event == "load_game_button":
                if self.__logged_in:

                    loaded_game_data = self.__db.load_game_state(self.__logged_in_username)

                    if not loaded_game_data:
                        sg.popup("No saved game found", title="Error Loading Game", keep_on_top=True)
                        continue

                    game_state_string, player2_name, player2_starts, player1pieces, player2pieces = loaded_game_data

                    if player2_name in self.__ai_name_to_level_num_map.values(): # if the player 2 name is an AI name
                        self.__ai_mode = True
                        self.__ai_name = player2_name


                    if self.__ai_mode:
                        ai_level = self.__ai_level_num_to_name_map[self.__ai_name]
                        self.__setup_match_page(self.__logged_in_username, self.__ai_name, ai_level=ai_level, game_state_string=game_state_string, player2_starts=player2_starts, player1_num_pieces=player1pieces, player2_num_pieces=player2pieces)

                    elif game_state_string and player2_name:
                        self.__setup_match_page(self.__logged_in_username, player2_name, game_state_string=game_state_string, player2_starts=player2_starts, player1_num_pieces=player1pieces, player2_num_pieces=player2pieces)

                    else:
                        sg.popup("No saved game found", title="Error Loading Game", keep_on_top=True)

                else:
                    sg.popup("You must be logged in to load a game", title="Error Loading Game", keep_on_top=True)



            elif event == "Show Login Status":
                if self.__logged_in_username:
                    sg.popup(f"Logged in as '{self.__logged_in_username}'", title="Logged In", keep_on_top=True)
                else:
                    sg.popup("Not logged in", title="Not Logged In", keep_on_top=True)

            elif event == "login_button":
                self.__login_window = self.__make_login_or_signup_window("login")

            elif event == "login_submit_button":
                username, password = values["login_username_input"], values["login_password_input"]

                if self.__db.login(username, password):
                    sg.popup("Logged in", title="Logged In", keep_on_top=True)

                    self.__logged_in_username = username
                    self.__logged_in = True

                    self.__preferred_piece_colour = self.__db.get_preferred_piece_colour(username)

                    BoardConstants.set_player_colour(self.__preferred_piece_colour, 1)

                    if self.__preferred_piece_colour == "green":
                        BoardConstants.set_player_colour("yellow", 2)

                    self.__login_window.close()

                else:
                    sg.popup("Incorrect username or password", title="Error Logging In", keep_on_top=True)



            elif event == "signup_button":
                self.__signup_window = self.__make_login_or_signup_window("signup")

            elif event == "signup_submit_button":
                username, password = values["signup_username_input"], values["signup_password_input"]

                if self.__db.check_if_username_exists(username):
                    sg.popup("Username already exists", title="Error Signing Up", keep_on_top=True)
                    
                else:
                    self.__db.add_user(username, password, values["piece_colour_choice"])
                    sg.popup("Account created", title="Account Created", keep_on_top=True)
                    self.__signup_window.close()

            elif event == "AI_play_button":
                self.__toggle_play_inputs("AI_play_inputs")

            elif event == "local_play_button":
                self.__toggle_play_inputs("local_play_inputs")

            elif event == "submit_local_play_button":

                player_1_name = self.__get_player1_name()
                self.__setup_match_page(player_1_name, values["player_2_local_input"])

            elif event == "submit_AI_play_button":
                difficulty_level = int(values['difficulty_slider'])
                self.__ai_name = self.__difficulty_level_to_ai_name(difficulty_level)
                self.__ai_mode = True

                player_1_name = self.__get_player1_name()

                self.__setup_match_page(player_1_name, self.__ai_name, ai_level=difficulty_level)

            elif event == "show_board_button":
                self.__display_board_window = self.__make_display_board_window()

                disp_win_open = True
                
                # thie needs to be here directly and not in a method for pysimplegui to display the image
                image_path = 'blank_board.png'
                image = Image.open(image_path)
                image.thumbnail((400, 400))  # Resize the image to fit the canvas
                background_img = ImageTk.PhotoImage(image)
                
                canvas = self.__display_board_window['-CANVAS-']
                
                canvas.TKCanvas.create_image(235, 215, image=background_img , anchor="center")
                
                self.__draw_pieces_on_disp_board(self.__display_board_window)


            elif event == "undo_move_button":
                self.__undo_move(self.__ai_mode)

                if disp_win_open:
                    self.__draw_pieces_on_disp_board(self.__display_board_window)

            elif self.__is_board_position(event):
                self.__toggle_highlight_board_position(event)

            elif event == "Home":
                self.__main_window.close()
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

                if disp_win_open:
                    self.__draw_pieces_on_disp_board(self.__display_board_window)

        self.__main_window.close()