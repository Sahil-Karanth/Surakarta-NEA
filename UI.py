from Game import Game
from utility_functions import oneD_to_twoD_array
import re
from MultiClassBoardAttributes import MultiClassBoardAttributes
import PySimpleGUI as sg
import textwrap
import time
from PIL import ImageTk, Image
from Database import Database

# todo
    # make easy AI not randomly move back into a corner

# ! to add to coursework document:


# ? to ask:
    # in the Board class' get_loc_single_capture method is the repeated code okay
        # slight difference which might make the method code long/confusing if I try and make it more general


class UI:

    """Abstract class for the UI. The play_game method is the method called to start the UI"""

    def __init__(self):
        self.__UI_type = None

        # a Game object
        self.__game = None

    def get_UI_type(self):
        raise NotImplementedError
    
    def play_game(self):
        raise NotImplementedError
  
class Graphical_UI(UI):

    """Graphical User Interface class for the game. Inherits from the UI class."""

    BUTTON_SIZE = 30
    FONT = "Helvetica"
    TITLE_FONT_SIZE = 60
    BUTTON_DIMENSIONS = (10, 1)
    COLUMN_PAD = 12
    LOGIN_PAD = 10
    PARAGRAPH_FONT_SIZE = 15

    HOME_BUTTON_PAD = (15, 10)
    BUTTON_FRAME_BORDER_WIDTH = 3

    SUBHEADING_FONT_PARAMS = (FONT, PARAGRAPH_FONT_SIZE, "bold")
    PARAGRAPH_FONT_PARAMS = (FONT, PARAGRAPH_FONT_SIZE)
    SUBMIT_BUTTON_FONT_PARAMS = (FONT, 15)

    LOGIN_WINDOW_HEIGHT = 270
    SIGNUP_WINDOW_HEIGHT = 350

    SLIDER_SIZE = (40, 15)
    GAME_MODE_BUTTON_PAD = (100, 100)

    PIECE_BUTTON_PAD = (30, 30)

    LOAD_GAME_INPUT_PAD = (200, COLUMN_PAD)

    DISP_BOARD_WINDOW_SIZE = (500, 400)
    DISP_BOARD_PIECE_SPACING = 43
    DISP_BOARD_INITAL_X = 128
    DISP_BOARD_INITAL_Y = 109
    DISP_BOARD_PIECE_RADIUS = 15

    STATS_WINDOW_SIZE = (500, 500)

    AVAILABLE_PIECE_COLOURS = ["yellow", "green", "red", "lightblue", "orange", "black"]
    AI_RESERVED_NAMES = ["Easy AI", "Medium AI", "Hard AI"]

    PIECE_IMAGES_PATH = "images/piece_images/"
    BOARD_IMAGES_PATH = "images/board_images/"

    def __init__(self):
        super().__init__()
        
        self.__UI_type = "GRAPHICAL"

        with open("help_page_text", "r") as f:
            
            self.__about_surakarta_text = textwrap.fill(f.readline(), 140)
            self.__rules_text = textwrap.fill(f.readline(), 140)


        sg.theme('Dark')

        self.__highlighted_board_positions = [] # stores board positions that the user has clicked on

        # windows
        self.__main_window = None
        self.__display_board_window = None
        self.__login_window = None
        self.__signup_window = None
        self.__load_game_window = None
        self.__change_piece_colour_window = None
        
        # login status variables
        self.__logged_in = False
        self.__logged_in_username = None 
        # self.__piece_colour = None

        # game variables
        self.__game = None
        self.__game_is_loaded = False
        self.__ai_mode = False
        self.__ai_name = None

        # display board background image
        self.__disp_board_background_img = None # needed to combat the python garbage collector

        # database object
        self.__db = Database("database.db")
        self.__saved_games = None # stored to enable deletion of saved games

        # maps difficulty level numbers to AI level names
        self.__ai_name_to_level_num_map = {
            1: "Easy AI",
            2: "Medium AI",
            3: "Hard AI"
        }

        # maps AI level names to difficulty level numbers
        self.__ai_level_num_to_name_map = {
            "Easy AI": 1,
            "Medium AI": 2,
            "Hard AI": 3
        }

        self.__current_page = None
        self.__setup_home_page()

    def __create_window(self, title, layout, justification, maximise=True, size=(700, 700), modal=False, disable_close=False, keep_on_top=False):

        """Creates a window with the given parameters"""

        window = sg.Window(
            title=title,
            layout=layout,
            size=size,
            resizable=False,
            keep_on_top=keep_on_top,
            modal=modal,
            disable_close=disable_close,          
            element_justification=justification,
            text_justification=justification
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

        """Creates the home page window. This is the first window that is displayed when the program is run."""

        new_game_button = sg.Button("New Game", pad=self.HOME_BUTTON_PAD, font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="new_game_button")
        load_game_button = sg.Button("Load Game", pad=self.HOME_BUTTON_PAD, font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="load_game_button")
        show_stats_button = sg.Button("Show Stats", pad=self.HOME_BUTTON_PAD, font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="show_stats_button")
        login_button = sg.Button("Login", pad=self.HOME_BUTTON_PAD, font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="login_button")
        signup_button = sg.Button("Sign Up", pad=self.HOME_BUTTON_PAD, font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="signup_button")
        help_button = sg.Button("Help", pad=self.HOME_BUTTON_PAD, font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="help_button")

        buttons_layout = [
            [new_game_button, login_button],
            [load_game_button, signup_button],
            [show_stats_button, help_button],
        ]

        # surround buttons with a frame
        buttons_frame = sg.Frame(title="", layout=buttons_layout, border_width=self.BUTTON_FRAME_BORDER_WIDTH, pad=(0, self.COLUMN_PAD))

        layout = [
            [self.__create_menu()],
            [sg.Text("Surakarta", pad=(0, self.COLUMN_PAD), font=(self.FONT, self.TITLE_FONT_SIZE))],
            [buttons_frame]
        ]

        if self.__main_window:
            self.__main_window.close()

        self.__current_page = "home_page"
        self.__main_window = self.__create_window("Surakarta", layout, "center")
    
    def __create_menu(self):

        """Creates the menu bar that is displayed at the top of every main non-modal window"""

        menu_layout = [
            ["Utilities", ["Home", "Show Login Status", "Logout", "Change Piece Colour", "Quit"]],
            ["Match Options", ["Restart Match", "Save Game"]]
        ]

        return sg.Menu(menu_layout, pad=(0, self.COLUMN_PAD))
    
    def __make_change_piece_colour_window(self):

        """Creates the change piece colour window which lets a logged in user change their piece colour"""

        layout = [
            [sg.Text("piece colour", pad=(0, self.LOGIN_PAD), font=self.PARAGRAPH_FONT_PARAMS)],
            [sg.Combo(self.AVAILABLE_PIECE_COLOURS, font=self.PARAGRAPH_FONT_PARAMS, expand_x=True, enable_events=True,  readonly=True, key="piece_colour_choice")],
            [sg.Button("Submit", pad=(0, self.COLUMN_PAD), font=self.SUBMIT_BUTTON_FONT_PARAMS, size=self.BUTTON_DIMENSIONS, key="submit_change_piece_colour_button")]
        ]

        return self.__create_window("Change Piece Colour", layout, "center", modal=True, keep_on_top=True, size=(300, 150), maximise=False, disable_close=False)

    def __make_login_or_signup_window(self, login_or_signup):
            
        """if login_or_signup is "login", creates the login window. If login_or_signup is "signup", creates the signup window"""

        if login_or_signup not in ["login", "signup"]:
            raise ValueError("login_or_signup parameter of the __make_login_or_signup_window method must be either 'login' or 'signup'")
            
        drop_down_menu_layout = []
        modal_height = self.LOGIN_WINDOW_HEIGHT

        if login_or_signup == "signup":

            # add piece colour dropdown menu to signup window
            drop_down_menu_layout = [
                [sg.Text("piece colour", pad=(0, self.LOGIN_PAD), font=self.PARAGRAPH_FONT_PARAMS)],
                [sg.Combo(self.AVAILABLE_PIECE_COLOURS, font=self.PARAGRAPH_FONT_PARAMS, expand_x=True, enable_events=True,  readonly=True, key="piece_colour_choice")]
            ]

            # signup window is taller than the login window because of the piece colour dropdown menu
            modal_height = self.SIGNUP_WINDOW_HEIGHT 
        
        layout = [
            [sg.Text("Username", pad=(0, self.LOGIN_PAD), font=self.PARAGRAPH_FONT_PARAMS)],
            [sg.InputText("", pad=(0, self.LOGIN_PAD), key=f"{login_or_signup}_username_input", font=self.PARAGRAPH_FONT_PARAMS)],
            [sg.Text("Password", pad=(0, self.LOGIN_PAD), font=self.PARAGRAPH_FONT_PARAMS)],
            [sg.InputText("", pad=(0, self.LOGIN_PAD), key=f"{login_or_signup}_password_input", password_char="*", font=self.PARAGRAPH_FONT_PARAMS)],
            [drop_down_menu_layout],
            [sg.Button("Submit", pad=(0, self.COLUMN_PAD), font=self.SUBMIT_BUTTON_FONT_PARAMS, size=self.BUTTON_DIMENSIONS, key=f"{login_or_signup}_submit_button")]
        ]

        return self.__create_window(login_or_signup.title(), layout, "center", modal=True, keep_on_top=True, size=(300, modal_height), maximise=False, disable_close=False)

    def __get_new_game_text_and_input_layout(self, disp_text, inp_default_text, inp_key):

        """Returns a layout containing a text element and an input element"""

        layout = [
            [sg.Text(disp_text, pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [sg.InputText(inp_default_text, pad=(0, self.COLUMN_PAD), key=inp_key, font=self.PARAGRAPH_FONT_PARAMS)],
        ]

        return layout

    def __setup_new_game_page(self):
        
        """Creates the new game page window where a user can choose to play a local or AI game, enter the names of the player(s) and choose the AI difficulty (if playing an AI game)"""
        
        # player 1's name is the logged in user's name if they are logged in, otherwise it is entered by the user
        player_1_input_visible = not self.__logged_in

        # player 1 name input layout for AI play
        player_1_input_AI_layout = self.__get_new_game_text_and_input_layout("Player 1 Name", "Player 1", "player_1_AI_input")

        # adding the player 1 name input layout to a column for formatting purposes
        player_1_AI_input_col = sg.Column(player_1_input_AI_layout, visible=player_1_input_visible)

        AI_input_layout = [
            [sg.Text("Difficulty", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [sg.Slider(range=(1, 3), default_value=1, orientation="h", size=self.SLIDER_SIZE, pad=(0, self.COLUMN_PAD), key="difficulty_slider")],
            [player_1_AI_input_col],
        ]

        # main column for the AI play inputs
        AI_input_col = sg.Column(key="AI_play_inputs", layout=AI_input_layout, pad=(0, self.COLUMN_PAD), visible=False)

        # player 1 name input layout for local play
        player_1_input_local_layout = self.__get_new_game_text_and_input_layout("Player 1 Name", "Player 1", "player_1_local_input")

        # adding the player 1 name input layout to a column for formatting purposes
        player_1_local_input_col = sg.Column(player_1_input_local_layout, visible=player_1_input_visible)

        Local_input_layout = [
            [player_1_local_input_col],
            [sg.Text("Player 2 Name", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [sg.InputText("Player 2", pad=(0, self.COLUMN_PAD), key="player_2_local_input", font=self.PARAGRAPH_FONT_PARAMS)],
        ]

        # main column for the local play inputs
        Local_input_col = sg.Column(key="local_play_inputs", layout=Local_input_layout, pad=(0, self.COLUMN_PAD), visible=False)

        # main page layout
        layout = [
            [self.__create_menu()],
            [sg.Button("Local Play", font=(self.FONT, self.BUTTON_SIZE), pad=self.GAME_MODE_BUTTON_PAD, size=self.BUTTON_DIMENSIONS, key="local_play_button"), sg.Button("AI Play", font=(self.FONT, self.BUTTON_SIZE), pad=self.GAME_MODE_BUTTON_PAD, size=self.BUTTON_DIMENSIONS, key="AI_play_button")],
            [AI_input_col, Local_input_col],
            [sg.Button("Submit", font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="submit_local_play_button", visible=False), sg.Button("Submit", font=(self.FONT, self.BUTTON_SIZE), size=self.BUTTON_DIMENSIONS, key="submit_AI_play_button", visible=False)],
        ]

        self.__main_window.close() # close the previous window (home page)
        self.__current_page = "new_game_page"
        self.__main_window = self.__create_window("New Game", layout, "center")

    def __setup_help_page(self):

        """Creates the help page window where the rules of the game are displayed"""

        text_layout = [
            [sg.Text("What is Surakarta?", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [sg.Text(self.__about_surakarta_text, pad=(0, self.COLUMN_PAD), font=self.PARAGRAPH_FONT_PARAMS)],
            [sg.Text("Rules", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [sg.Text(self.__rules_text, pad=(0, self.COLUMN_PAD), font=self.PARAGRAPH_FONT_PARAMS)],
        ]

        layout = [
            [self.__create_menu()],
            [text_layout],
            [sg.Image(f"{self.BOARD_IMAGES_PATH}starting_board.png", expand_x=True, expand_y=True)],
        ]

        self.__main_window.close() # close the previous window (home page)
        self.__current_page = "help_page"
        self.__main_window = self.__create_window("Help Page", layout, "center")

    def __toggle_new_game_input_visibility(self, key_to_make_visible):

        """Toggles the visibility of the AI play inputs and the local play inputs. When the AI play inputs are visible, the local play inputs are not and vice versa"""

        # these two lists contain the keys of the elements that need to be toggled
        local_play_element_keys = ["local_play_inputs", "submit_local_play_button"]
        AI_play_element_keys = ["AI_play_inputs", "submit_AI_play_button"]

        if key_to_make_visible == "AI_play_inputs":
            AI_visible = True
            local_visible = False

        elif key_to_make_visible == "local_play_inputs":
            AI_visible = False
            local_visible = True
        
        else:
            raise ValueError("key_to_make_visible parameter of the __toggle_new_game_input_visibility method must be either 'AI_play_inputs' or 'local_play_inputs'")


        # make the elements visible or invisible
        for key in local_play_element_keys:
            self.__main_window[key].update(visible=local_visible)

        for key in AI_play_element_keys:
            self.__main_window[key].update(visible=AI_visible)

    def __make_piece_button(self, piece_type, key, visible=False):

        """Creates a button used to represent a board piece with the given piece type and key. The button is invisible by default"""

        return sg.Button("", image_filename=f"{self.PIECE_IMAGES_PATH}{piece_type}_counter.png", pad=self.PIECE_BUTTON_PAD, visible=visible, key=key, button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0)

    def __create_table(self, database_table_data, headers, key):

        """Creates a table with the given rows and headers"""

        rows = [[element for element in row] for row in database_table_data]

        return sg.Table(rows, headings=headers, expand_x=True, background_color="light gray", text_color="black", key=key)
    
    @staticmethod
    def __create_circle(canvas, x, y, radius, fill):

        """Creates a circle on the given Tkinter canvas with the given radius, fill colour and centre coordinates.
        Method credit to https://stackoverflow.com/questions/17985216/draw-circle-in-tkinter-python"""

        # oval coordinates are given as the top left and bottom right coordinates of the bounding box
        x0 = x - radius
        y0 = y - radius
        x1 = x + radius
        y1 = y + radius
        
        return canvas.create_oval(x0, y0, x1, y1, fill=fill, outline="black", tags="counter")

    def __draw_pieces_on_disp_board(self):

        """Draws the pieces on the display board window"""

        # underlying Tkinter canvas
        canvas = self.__display_board_window['-CANVAS-'].TKCanvas

        # delete all existing drawn pieces
        canvas.delete("counter")

        # 6x6 2D array of the board state where each element is a string representing the colour of the piece
        display_board = [[i.get_colour() for i in row] for row in self.__game.get_board_state()]

        for i, row in enumerate(display_board):
            for j, counter in enumerate(row):

                if counter == None: # don't draw a piece if there is no piece at that location
                    continue
                
                else:
                    # new centre cords can be calculated from the piece at (0,0)'s cords and the spacing between pieces as the board is square shaped
                    centre_x = self.DISP_BOARD_INITAL_X + (self.DISP_BOARD_PIECE_SPACING * j)
                    centre_y = self.DISP_BOARD_INITAL_Y + (self.DISP_BOARD_PIECE_SPACING * i)
                    self.__create_circle(canvas, centre_x, centre_y, self.DISP_BOARD_PIECE_RADIUS, counter)

    def __make_display_board_window(self):

        """Creates the display board window where the user can view the board state of the current game including the looped tracks around the board". The canvas is initially empty"""

        # prevents the display board window from being opened multiple times (making the window modal would prevent the user from moving pieces while the display board is open)
        if self.__display_board_window: 
            self.__display_board_window.close()

        layout = [
            [sg.Canvas(size=self.DISP_BOARD_WINDOW_SIZE, key='-CANVAS-')],
        ]

        display_board_window = self.__create_window("Display Board", layout, "center", size=self.DISP_BOARD_WINDOW_SIZE, maximise=False, modal=False, disable_close=False, keep_on_top=True)

        return display_board_window
    
    def __make_load_game_window(self):

        """Creates the load game window where the user can load a saved game or delete a saved game. A table is displayed showing the user's saved games."""

        if not self.__logged_in:
            sg.popup("You must be logged in to load a game", title="Error Loading Game", keep_on_top=True)
            return

        # request the user's saved games from the database
        self.__saved_games = self.__db.load_saved_games(self.__logged_in_username)
        saved_games_table_headers = ["Game ID", "Date", "Opponent"]

        saved_games_table = self.__create_table(self.__saved_games, saved_games_table_headers, "saved_games_table")
            
        layout = [
            [sg.Text("Enter a Game ID to Load", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [sg.Input("", pad=self.LOAD_GAME_INPUT_PAD, key="loading_game_id_input", font=self.PARAGRAPH_FONT_PARAMS, justification="center")],
            [sg.Button("Load", pad=(0, self.COLUMN_PAD), font=self.SUBMIT_BUTTON_FONT_PARAMS, size=self.BUTTON_DIMENSIONS, key="submit_loading_game_id_button")],
            [saved_games_table],
            [sg.Text("Enter a Game ID to Delete", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [sg.Input("", pad=self.LOAD_GAME_INPUT_PAD, key="deleting_game_id_input", font=self.PARAGRAPH_FONT_PARAMS, justification="center")],
            [sg.Button("Delete", pad=(0, self.COLUMN_PAD), font=self.SUBMIT_BUTTON_FONT_PARAMS, size=self.BUTTON_DIMENSIONS, key="submit_deleting_game_id_button")],
        ]

        load_game_window = self.__create_window("Load Game", layout, "center", size=(500, 550), maximise=False, modal=True, disable_close=False, keep_on_top=True)

        return load_game_window

    def __make_stats_window(self):

        """Creates the stats window where the user can view their match stats and game history"""

        # request the user's match stats and game history from the database
        ai_match_stats = self.__db.get_user_stats(self.__logged_in_username)
        ai_stats_table_headers = ["AI Difficulty", "Wins", "Losses"]

        ai_stats_table = self.__create_table(ai_match_stats, ai_stats_table_headers, "ai_stats_table")

        # request the user's game history from the database
        game_history = self.__db.get_user_game_history(self.__logged_in_username)
        game_history_table_headers = ["Game Number", "Date", "Opponent", "Winner"]

        game_history_table = self.__create_table(game_history, game_history_table_headers, "game_history_table")

        layout = [
            [sg.Text("AI Match Stats", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [ai_stats_table],
            [sg.Text("Game History", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS)],
            [game_history_table],
        ]

        stats_window = self.__create_window("Stats", layout, "center", size=self.STATS_WINDOW_SIZE, maximise=False, modal=False, disable_close=False, keep_on_top=True)

        return stats_window

    def __setup_match_page(self, player1name, player2name, ai_level=None, game_state_string=None, player2_starts=False, player1_num_pieces=MultiClassBoardAttributes.NUM_STARTING_PIECES_EACH, player2_num_pieces=MultiClassBoardAttributes.NUM_STARTING_PIECES_EACH):

        """Creates the match page window where the user can play a game of Surakarta. The board state is displayed and the user can move pieces by clicking on the board"""

        # create the Game object
        self.__create_game_object(player1name, player2name, ai_level, game_state_string, player2_starts, player1_num_pieces, player2_num_pieces)

        if game_state_string:
            self.__game_is_loaded = True

        # 6x6 2D array of the board state where each element is a string representing the colour of the piece
        board_colours = [[i.get_colour() for i in row] for row in self.__game.get_board_state()]

        # layout to show the board state
        board_layout = []

        for i, row in enumerate(board_colours):
            for j, colour in enumerate(row):
                
                key = f"{i},{j}" # unique key for each piece button

                if colour == None: # blank location (shown with a small white dot)
                    button = self.__make_piece_button("blank", key, visible=True)

                else:
                    button = self.__make_piece_button(colour, key, visible=True)

                board_layout.append(button)

        # make the board_layout the same shape as the actual board (6x6 2D array)
        board_layout = oneD_to_twoD_array(board_layout, len(board_colours))

        # text to show whose turn it is
        player_turn_layout = [
            [sg.Text(f"{self.__game.get_player_name(1)}'s Turn", key="player1_turn_text", pad=(0, self.COLUMN_PAD), font=self.SUBHEADING_FONT_PARAMS, visible=True)],
            [sg.Text(f"{self.__game.get_player_name(2)}'s Turn", key="player2_turn_text", pad=(0, self.COLUMN_PAD), font=self.PARAGRAPH_FONT_PARAMS, visible=False)],
        ]

        # current player turn in a frame for formatting purposes
        player_turn_frame = sg.Frame("", layout=player_turn_layout, border_width=0)

        # radio buttons to select the move type (capture or normal move)
        move_option = sg.Radio("Move", key="move_type_radio_move", group_id="move_type_radio", font=self.SUBHEADING_FONT_PARAMS)
        capture_option = sg.Radio("Capture", key="move_type_radio_capture", group_id="move_type_radio", font=self.SUBHEADING_FONT_PARAMS)

        submit_move_button = sg.Button("Submit Move", font=(self.FONT, 15), key="submit_move_button")
        undo_move_button = sg.Button("Undo Move", font=(self.FONT, 15), key="undo_move_button")

        # button to show the display board window
        show_display_board_button = sg.Button("show board", key="show_board_button", font=(self.FONT, 15))

        # text to show the number of pieces captured by each player
        pieces_captured_player1_text = self.__get_pieces_captured_display_text(1)
        pieces_captured_player2_text = self.__get_pieces_captured_display_text(2)

        # layout to show the number of pieces captured by each player
        player1_captured_layout = [[sg.Text(pieces_captured_player1_text, key="player1_captured_text", font=self.PARAGRAPH_FONT_PARAMS, pad=(50, 0))]]
        player2_captured_layout = [[sg.Text(pieces_captured_player2_text, key="player2_captured_text", font=self.PARAGRAPH_FONT_PARAMS, pad=(50, 0))]]
        
        # main layout for the match page
        layout = [
            [self.__create_menu()],
            [player_turn_frame],
            [show_display_board_button],
            [undo_move_button, move_option, capture_option, submit_move_button],
            [sg.Column(player1_captured_layout), sg.Column(board_layout), sg.Column(player2_captured_layout)],
        ]

        self.__main_window.close() # close the previous window (new game page)
        self.__current_page = "match_page"
        self.__main_window = self.__create_window("Match", layout, "center")

        if player2_starts: # player 2 can start if the game is being loaded (i.e. not a new game)
            self.__update_current_player_display(self.__game_is_loaded)
            self.__update_number_captured_pieces_display()

    def __update_number_captured_pieces_display(self):

        """Updates the text showing the number of pieces captured by each player on the match page"""

        self.__main_window["player1_captured_text"].update(self.__get_pieces_captured_display_text(1))
        self.__main_window["player2_captured_text"].update(self.__get_pieces_captured_display_text(2))

    def __get_pieces_captured_display_text(self, player_number):
            
            """Returns a string containing the number of pieces captured by the given player"""

            if player_number == 1:
                other_player_num = 2
            
            elif player_number == 2:
                other_player_num = 1

            else:
                raise ValueError("player_number parameter of the __get_pieces_captured_display_text method must be either 1 or 2")

            # calculate the number of pieces captured by the player (starting pieces - pieces left for the other player)
            player_num_captured = MultiClassBoardAttributes.NUM_STARTING_PIECES_EACH - self.__game.get_player_piece_count(other_player_num)

            # textwrap the player names to prevent the text from being too long and pushing the board off the screen
            text_wrapped_player_name = textwrap.fill(self.__game.get_player_name(player_number), 10)
    
            return f"{text_wrapped_player_name} captured pieces: {player_num_captured}"

    def __update_game_and_UI_after_move(self, start_loc, end_loc, move_type):

        """updates the game object and the match page GUI after a move has been made"""

        # move object reprsenting the move that was made on the Board object
        move_obj = self.__game.make_and_return_move(start_loc, end_loc, move_type)

        # updating the UI with the move object
        self.__update_board_display_after_move(move_obj.get_start_cords(), move_obj.get_end_cords(), move_obj.get_start_colour())

        # update GUI and game object with the new current player
        self.__update_current_player_display()
        self.__game.switch_current_player()

    def __make_move_on_display(self, values, ai_mode=False):

        """Makes the move on the GUI board and the game object's board if the move is legal"""

        # if the user has not selected a start and end location, return
        if len(self.__highlighted_board_positions) != 2:
            sg.popup("Please select a start and end location", keep_on_top=True)
            return

        # convert the start and end locations from coordinate strings to coordinate tuples
        start_cords = self.__str_key_to_cords_tuple(self.__highlighted_board_positions[0])
        end_cords = self.__str_key_to_cords_tuple(self.__highlighted_board_positions[1])
        
        # get corresponding GridLocation objects from the game object's board
        start_loc = self.__game.get_board_state()[start_cords[0]][start_cords[1]]
        end_loc = self.__game.get_board_state()[end_cords[0]][end_cords[1]]

        # getting the move type from the radio buttons
        if values["move_type_radio_move"]:
            move_type = MultiClassBoardAttributes.NORMAL_MOVE_TYPE
        
        elif values["move_type_radio_capture"]:
            move_type = MultiClassBoardAttributes.CAPTURE_MOVE_TYPE

        else:
            sg.popup("Please select a move type", keep_on_top=True)

            # unhighlight the selected locations
            self.__toggle_highlight_board_position(self.__highlighted_board_positions[1])
            self.__toggle_highlight_board_position(self.__highlighted_board_positions[0])
            return
        
        # prev_move_legal is used to determine whether the AI should make a move after the user has made a move
        prev_move_legal = True

        if self.__game.is_legal_move(start_loc, end_loc, move_type): # check if the attempted move is legal

            # make move on board and GUI
            self.__update_game_and_UI_after_move(start_loc, end_loc, move_type)

            if move_type == MultiClassBoardAttributes.CAPTURE_MOVE_TYPE:
                self.__update_number_captured_pieces_display() # update the number of pieces captured by each player
                self.__end_if_game_over() # check if human has won --> only need to check if the game is over after a capture move
            
        else:
            sg.popup("ILLEGAL MOVE", keep_on_top=True)
            prev_move_legal = False # the AI should not make a move if the user's move was illegal

        # unhighlight the selected locations
        self.__toggle_highlight_board_position(self.__highlighted_board_positions[1])
        self.__toggle_highlight_board_position(self.__highlighted_board_positions[0])

        if ai_mode and prev_move_legal:
            move = self.__game.get_ai_move() # get the AI's move

            # make the AI's move on the board and GUI
            self.__update_game_and_UI_after_move(move.get_start_loc(), move.get_end_loc(), move.get_move_type())

            if move.get_move_type() == MultiClassBoardAttributes.CAPTURE_MOVE_TYPE:
                self.__update_number_captured_pieces_display()
                self.__end_if_game_over() # check if AI has won

    def __reset_game_variables(self):

        """Resets the match variables to their initial values"""

        self.__game = None
        self.__game_is_loaded = False
        self.__ai_mode = False
        self.__ai_name = None
        self.__highlighted_board_positions = []

    def __end_if_game_over(self):

        """Uses the game object's set_game_status method to update the game's status and ends the game with a popup if necessary"""

        # update the game's status using the number of pieces left on the board
        self.__game.set_game_status()

        if self.__game.is_game_over():
            winning_player = self.__game.get_winning_player()

            sg.popup(f"{winning_player.get_name()} has won the game!", title="Game Over", keep_on_top=True)

            # if the user is logged need to add the game to their history and update their stats (if the match was against an AI)
            if self.__logged_in and self.__ai_mode:

                human_won = False

                if winning_player.get_name() == self.__logged_in_username:
                    human_won = True

                # increment the user's win/loss count against the AI difficulty depending on whether they won or lost
                self.__db.update_user_stats(self.__logged_in_username, human_won, self.__ai_name)

            # remove the game from the database if it was loaded
            if self.__game_is_loaded:
                self.__db.delete_saved_game(self.__logged_in_username)

            # add game to game history if the user is logged in
            if self.__logged_in:
                self.__db.add_game_to_history(self.__logged_in_username, self.__game.get_player_name(2), winning_player.get_name())

            self.__reset_game_variables()
            self.__setup_home_page() # go back to the home page after a match has ended

    def __handle_change_piece_colour(self, new_piece_colour):
            
            """Changes the piece colour of the player. This method is used when a logged in user changes their piece colour"""

            # update the piece colours in the MultiClassBoardAttributes class (for the current running application)
            self.__update_piece_colour(new_piece_colour)
    
            # update the new piece colour in the database
            self.__db.update_stored_piece_colour(self.__logged_in_username, new_piece_colour)
            self.__change_piece_colour_window.close()
    
    def __handle_delete_saved_game(self, game_id):

        """Deletes the game with the given ID from the database provided that saved game data has been loaded and the user is logged in"""

        if not self.__saved_games:
            raise ValueError("Attempting to delete a saved game when save data has not been loaded from the database yet")

        if not self.__logged_in:
            raise ValueError("Attempting to delete a saved game when the user is not logged in")

        # list of game IDs of the user's saved games
        game_id_lst = [i[0] for i in self.__saved_games]

        # check if the game ID is valid (i.e. the user has a saved game with that ID)
        if int(game_id) not in game_id_lst:
            sg.popup(f"No game with that ID exists", title="Error Deleting Game", keep_on_top=True)
            return

        # delete the game from the database
        self.__db.delete_saved_game(game_id)
        sg.popup("Game deleted", title="Game Deleted", keep_on_top=True)

        # update the table to not show the deleted game
        self.__load_game_window["saved_games_table"].update(values=self.__db.load_saved_games(self.__logged_in_username))

    def __handle_load_game(self, game_id):

        """Loads the game with the given ID from the database and sets up the match page with the loaded game data"""

        # load game data from the database
        loaded_game_data = self.__db.load_game_state(game_id)

        if not loaded_game_data:
            sg.popup(f"No game with that ID exists", title="Error Loading Game", keep_on_top=True)
            return
        
        # make instance variable to allow the game to be deleted from the database if the user saves the game again in the __handle_save_game method
        self.__loaded_game_id = game_id

        # unpack the loaded game data
        game_state_string, player2_name, player2_starts, player1pieces, player2pieces, player1_colour = loaded_game_data

        # update the player 1 colour in the MultiClassBoardAttributes class to be the colour that the user had when they saved the game
        self.__update_piece_colour(player1_colour)

        # if the player 2 name is an AI name, the game is an AI game
        if player2_name in self.__ai_name_to_level_num_map.values():
            self.__ai_mode = True
            self.__ai_name = player2_name

            # use the AI name to get the AI level and set up the match page
            ai_level = self.__ai_level_num_to_name_map[self.__ai_name]
            self.__setup_match_page(self.__logged_in_username, self.__ai_name, ai_level=ai_level, game_state_string=game_state_string, player2_starts=player2_starts, player1_num_pieces=player1pieces, player2_num_pieces=player2pieces)

        # if the player 2 name is not an AI name, the game is a local game
        elif game_state_string and player2_name:
            self.__setup_match_page(self.__logged_in_username, player2_name, game_state_string=game_state_string, player2_starts=player2_starts, player1_num_pieces=player1pieces, player2_num_pieces=player2pieces)

        else:
            sg.popup(f"No game with id {game_id} could be found", title="Error Loading Game", keep_on_top=True)

        self.__load_game_window.close()

    def __handle_logout(self):

        """Logs the user out if they are logged in and on the home page. Otherwise, displays an error message"""

        if self.__logged_in:
            self.__logged_in = False
            self.__logged_in_username = None

            # reset the player 1 piece colour to the default colour
            self.__update_piece_colour(MultiClassBoardAttributes.DEFAULT_PLAYER_1_COLOUR)

            sg.popup("Logged out", title="Logged Out", keep_on_top=True)

        elif self.__current_page != "home_page":
            sg.popup("You can only logout from the home page", title="Error Logging Out", keep_on_top=True)

        else:
            sg.popup("You are not logged in", title="Error Logging Out", keep_on_top=True)

    def __handle_save_game(self):

        """Saves the current game state to the database if the user is logged in and on the match page. Otherwise, displays an error message"""

        if self.__current_page == "match_page" and self.__logged_in:

            # if saving a loaded game, delete the old game from the database and replace it with the new game
            if self.__game_is_loaded:
                self.__db.delete_saved_game(self.__loaded_game_id)

            # serialise the game state to a string to store in the database
            game_state_string = self.__game.get_game_state_string()

            # determine if player 2 should start when the game is loaded again
            player2_starts = self.__game.get_player_name(2) == self.__game.get_current_player_name()

            # save the game to the database
            self.__db.save_game_state(self.__logged_in_username, game_state_string, self.__game.get_player_name(2), player2_starts, self.__game.get_player_piece_count(1), self.__game.get_player_piece_count(2), MultiClassBoardAttributes.player_1_colour)
            sg.popup("Game saved", title="Game Saved", keep_on_top=True)

        else:
            sg.popup("You can only save a game from the match page", title="Error Saving Game", keep_on_top=True)

    def __update_piece_colour(self, new_colour):

        """Updates the piece colour of the player. This method is used when a logged in user changes their piece colour"""

        MultiClassBoardAttributes.set_player_colour(new_colour, 1)

        # since green is the default colour for player 2, if player 1's colour is changed to green, player 2's colour should be changed to yellow
        if new_colour == "green":
            MultiClassBoardAttributes.set_player_colour("yellow", 2)

        # since yellow is the default colour for player 2, if player 1's colour is changed to yellow, player 2's colour should be changed to green
        elif new_colour == "yellow":
            MultiClassBoardAttributes.set_player_colour("green", 2)

    def __handle_login(self, username, password):

        """Attempts to log the user in with the given username and password. Displays an error message if the username or password is incorrect"""

        if self.__db.login(username, password):
            sg.popup("Logged in", title="Logged In", keep_on_top=True)

            self.__logged_in_username = username
            self.__logged_in = True

            # query the database for the user's piece colour and update the piece colours in the MultiClassBoardAttributes class
            piece_colour = self.__db.get_piece_colour(username)
            self.__update_piece_colour(piece_colour)

            self.__login_window.close()

        else:
            sg.popup("Incorrect username or password", title="Error Logging In", keep_on_top=True)

    def __handle_sign_up(self, username, password, piece_colour):

        """Attempts to sign the user up with the given username and password. Displays an error message if the username is already taken or if the username is reserved"""

        # ensures usernames are unique
        if self.__db.check_if_username_exists(username):
            sg.popup("Username already exists", title="Error Signing Up", keep_on_top=True)

        # username can't be one of the AI names (Easy AI, Medium AI, Hard AI)
        elif username in self.AI_RESERVED_NAMES:
            sg.popup("Username is reserved and cannot be used", title="Error Signing Up", keep_on_top=True)
            
        else:
            # add the user to the database
            self.__db.add_user(username, password, piece_colour)

            sg.popup("Account created", title="Account Created", keep_on_top=True)
            self.__signup_window.close()

    def __handle_showing_display_board(self):

        """Shows the display board window"""

        self.__display_board_window = self.__make_display_board_window()
        
        # loading the board image to be the background of the canvas
        image_path = f"{self.BOARD_IMAGES_PATH}blank_board.png"
        image = Image.open(image_path)

        # Resize the image to fit the canvas
        image.thumbnail((400, 400))

        # storing the image in an instance variable to prevent garbage collection
        self.__disp_board_background_img = ImageTk.PhotoImage(image)
        
        # add the background board image to the underlying Tkinter canvas
        canvas = self.__display_board_window['-CANVAS-']
        canvas.TKCanvas.create_image(235, 215, image=self.__disp_board_background_img , anchor="center")
        
        # draw the pieces on the board
        self.__draw_pieces_on_disp_board()

    def __handle_restart_match(self):

        """Restarts the match if the user is on the match page. Otherwise, displays an error message."""

        if self.__current_page == "match_page":
            # make a new game with the same player names
            player1_name = self.__game.get_player_name(1)
            player2_name = self.__game.get_player_name(2)

            ai_level = None
            if self.__ai_mode:
                ai_level = self.__ai_name_to_level_num_map[player2_name]
            
            self.__setup_match_page(player1_name, player2_name, ai_level=ai_level)

        else:
            sg.popup("You can only restart a match from the match page", title="Error Restarting Match", keep_on_top=True)

    def __show_login_status_popup(self):

        """Shows a popup displaying whether the user is logged in or not"""

        if self.__logged_in_username:
            sg.popup(f"Logged in as '{self.__logged_in_username}'", title="Logged In", keep_on_top=True)
        else:
            sg.popup("Not logged in", title="Not Logged In", keep_on_top=True)

    def __update_board_display_after_move(self, start_cords, end_cords, start_colour):

        """updates the GUI board display after a move has been made"""

        # convert the start and end locations from coordinate tuples to coordinate strings (the format of the GUI board piece element keys)
        start_cords_str = f"{start_cords[0]},{start_cords[1]}"
        end_cords_str = f"{end_cords[0]},{end_cords[1]}"

        # update the start and end location piece buttons on the GUI board with their new images
        self.__main_window[f"{start_cords_str}"].update(image_filename=f"{self.PIECE_IMAGES_PATH}blank_counter.png")   
        self.__main_window[f"{end_cords_str}"].update(image_filename=f"{self.PIECE_IMAGES_PATH}{start_colour}_counter.png")

    def __update_current_player_display(self, game_is_loaded=False):

        """updates the text showing whose turn it is on the match page. Updated after every move."""
        
        # the text element showing whose turn it is
        current_text = self.__main_window["player1_turn_text"]

        # switches the current player display to player 2's name if the game is loaded and it is player 2's turn immediately after loading the game
        if game_is_loaded and self.__game.get_current_player_name() == self.__game.get_player_name(2):
            current_text.update(f"{self.__game.get_player_name(2)}'s Turn")
            return

        # switch to player 2's turn
        if self.__game.get_current_player_name() == self.__game.get_player_name(1):
            current_text.update(f"{self.__game.get_player_name(2)}'s Turn")
        
        # switch to player 1's turn
        elif self.__game.get_current_player_name() == self.__game.get_player_name(2):
            current_text.update(f"{self.__game.get_player_name(1)}'s Turn")

    def __is_board_position(self, key):

        """checks if the given key is a valid board piece button (i.e. a key of the form 'x,y' where x and y are integers)"""

        # make sure the key is not None which would cause an error with the regex
        if not key:
            return False

        min_row_index = MultiClassBoardAttributes.MIN_ROW_INDEX
        max_row_index = MultiClassBoardAttributes.MAX_ROW_INDEX

        pattern = fr'^[{min_row_index}-{max_row_index}],[{min_row_index}-{max_row_index}]$'
        if bool(re.match(pattern, key)):
            return True
        
        return False
        
    def __str_key_to_cords_tuple(self, string_key):

        """converts a string key of a GUI element in the form 'x,y' to a tuple of the form (x,y) where x and y are integers"""

        return tuple(int(i) for i in string_key.split(","))
    
    def __cords_tuple_to_str_key(self, tuple_key):

        """converts a tuple key of the form (x,y) to a string of the form 'x,y' where x and y are integers"""

        return f"{tuple_key[0]},{tuple_key[1]}"
    
    def __get_player1_name(self, ai_mode):

        """returns the player 1 during a match. If the user is logged in, this is the logged in username."""

        if self.__logged_in:
            return self.__logged_in_username
        
        elif ai_mode:
            return self.__main_window["player_1_AI_input"].get()
        
        else:
            return self.__main_window["player_1_local_input"].get()
    
    def __toggle_highlight_board_position(self, key):

        """toggles the highlighting of a board position. If the position is already highlighted, unhighlights it. If it is not highlighted, highlights it.
        Positions are highlighted in pink. A maximum of two positions can be highlighted at once."""
        
        if not self.__is_board_position(key):
            raise ValueError("Attempting to highlight a non-board position")

        # piece button specified by the key parameter
        button = self.__main_window[key]

        # if the position is already highlighted, unhighlight it
        if key in self.__highlighted_board_positions:
            button.update(button_color=('pink', sg.theme_background_color()))
            self.__highlighted_board_positions.remove(key)

        # if the position is not highlighted, highlight it
        elif key not in self.__highlighted_board_positions and len(self.__highlighted_board_positions) < 2:
            button.update(button_color=(sg.theme_background_color(), 'pink'))
            self.__highlighted_board_positions.append(key)

    def __undo_move(self, ai_mode=False):

        """Undoes the last move made on the board and updates the GUI board display. If the last move was a capture move, the piece that was captured is restored to the board.
        If the last move was made by the AI, the move is undone twice to undo the AI's move and the human's move."""

        # the move object representing the move that was undone
        move_obj = self.__game.undo_move()

        if move_obj == None:
            sg.popup("No moves to undo", keep_on_top=True)
            return
        
        # update the GUI board display by making the last move in reverse
        self.__update_board_display_after_move(move_obj.get_end_cords(), move_obj.get_start_cords(), move_obj.get_start_colour())

        # if the last move was a capture move, restore the piece that was captured to the board GUI
        if move_obj.get_move_type() == MultiClassBoardAttributes.CAPTURE_MOVE_TYPE:            
            cords = self.__cords_tuple_to_str_key(move_obj.get_end_cords())
            self.__main_window[f"{cords}"].update(image_filename=f"{self.PIECE_IMAGES_PATH}{move_obj.get_end_colour()}_counter.png")

            # show the new number of pieces captured by each player
            self.__update_number_captured_pieces_display()

        # update the current player in game and on the GUI's display text
        self.__update_current_player_display()
        self.__game.switch_current_player()

        # if the last move was made by the AI, undo the move again to undo the AI's move
        if ai_mode:
            self.__undo_move()

    def __difficulty_level_to_ai_name(self, difficulty_level):
        
        """returns the AI name corresponding to the given difficulty level"""

        return self.__ai_name_to_level_num_map[difficulty_level]

    def __create_game_object(self, name1, name2, ai_level, game_state_string, player2_starts, player1pieces, player2pieces):

        """Creates a Game object with the given parameters and stores it in an instance variable"""

        self.__game = Game(name1, name2, ai_level=ai_level, game_state_string=game_state_string, player2_starts=player2_starts, player1_num_pieces=player1pieces, player2_num_pieces=player2pieces)

    def play_game(self):

        """The main event loop of the GUI. Handles all events and updates the GUI accordingly. This is the only public method of the UI class and is called by the main.py file to launch the application."""

        # boolean to keep track of whether the display board window is open
        disp_win_open = False

        while True:
            # read events and values from the all active windows
            window, event, values = sg.read_all_windows()

            # a window is closed
            if event == sg.WIN_CLOSED or event == 'Quit':

                # close the display board window if it is open
                if window == self.__display_board_window:
                    disp_win_open = False
                    self.__display_board_window.close()

                # terminate the application if the main window is closed
                elif window == self.__main_window:
                    window.close()
                    break

                else:
                    window.close()  

            # go to the new game page
            if event == "new_game_button": 
                self.__setup_new_game_page()                

            # go to the help page
            elif event == "help_button":
                self.__setup_help_page()

            # show the user's stats in a modal window
            elif event == "show_stats_button":
                if self.__logged_in_username:
                    self.__make_stats_window()

                else:
                    sg.popup("You must be logged in to view your stats", title="Error Showing Stats", keep_on_top=True)
            
            # save the game if the user is logged in and on the match page
            elif event == "Save Game": 
                self.__handle_save_game()

            # show the saved games modal window
            elif event == "load_game_button": 
                self.__load_game_window = self.__make_load_game_window()

            # load the game with the given ID
            elif event == "submit_loading_game_id_button":
                game_id = values["loading_game_id_input"]
                self.__handle_load_game(game_id)

            # delete the game with the given ID
            elif event == "submit_deleting_game_id_button":
                game_id = values["deleting_game_id_input"]
                self.__handle_delete_saved_game(game_id)

            # show the change piece colour modal window
            elif event == "Change Piece Colour":
                if self.__logged_in:
                    self.__change_piece_colour_window = self.__make_change_piece_colour_window()

                else:
                    sg.popup("You must be logged in to change your piece colour", title="Error Changing Piece Colour", keep_on_top=True)

            # change the piece colour of the logged in user
            elif event == "submit_change_piece_colour_button":
                new_colour = values["piece_colour_choice"]
                self.__handle_change_piece_colour(new_colour)

            # show the login status popup window
            elif event == "Show Login Status":
                self.__show_login_status_popup()

            # logout the user
            elif event == "Logout":
                self.__handle_logout()

            # show the login modal window
            elif event == "login_button":
                self.__login_window = self.__make_login_or_signup_window("login")

            # attempt to login the user
            elif event == "login_submit_button":
                username, password = values["login_username_input"], values["login_password_input"]
                self.__handle_login(username, password)

            # show the signup modal window
            elif event == "signup_button":
                self.__signup_window = self.__make_login_or_signup_window("signup")

            # attempt to sign the user up
            elif event == "signup_submit_button":
                username, password, piece_colour = values["signup_username_input"], values["signup_password_input"], values["piece_colour_choice"]
                self.__handle_sign_up(username, password, piece_colour)

            # show the AI play input fields and hide the local play input fields in the new game page
            elif event == "AI_play_button":
                self.__toggle_new_game_input_visibility("AI_play_inputs")

            # show the local play input fields and hide the AI play input fields in the new game page
            elif event == "local_play_button":
                self.__toggle_new_game_input_visibility("local_play_inputs")

            # submit the local play input fields and set up the match page
            elif event == "submit_local_play_button":
                player_1_name = self.__get_player1_name(ai_mode=False)
                self.__setup_match_page(player_1_name, values["player_2_local_input"])

            # submit the AI play input fields and set up the match page
            elif event == "submit_AI_play_button":
                difficulty_level = int(values['difficulty_slider'])
                self.__ai_name = self.__difficulty_level_to_ai_name(difficulty_level)
                self.__ai_mode = True

                player_1_name = self.__get_player1_name(ai_mode=True)

                self.__setup_match_page(player_1_name, self.__ai_name, ai_level=difficulty_level)

            # show the display board window in a match
            elif event == "show_board_button":
                disp_win_open = True
                self.__handle_showing_display_board()

            # undo the last move in a match
            elif event == "undo_move_button":
                self.__undo_move(self.__ai_mode)

                # redraw the pieces on the display board if it is open
                if disp_win_open:
                    self.__draw_pieces_on_disp_board()

            # highlight a board position if it is not already highlighted. If it is already highlighted, unhighlight it
            elif self.__is_board_position(event):
                self.__toggle_highlight_board_position(event)

            # go back to the home page
            elif event == "Home":
                self.__main_window.close()
                self.__setup_home_page()

            # restart the match
            elif event == "Restart Match":
                self.__handle_restart_match()

            # make a move in a match
            elif event == "submit_move_button":
                self.__make_move_on_display(values, self.__ai_mode)

                # redraw the pieces on the display board if it is open
                if disp_win_open:
                    self.__draw_pieces_on_disp_board()

        self.__main_window.close()

class Terminal_UI(UI):
    
    """Terminal user interface for the game. Inherits from the UI class. Only supports local play."""

    # constants used to display the board
    EMPTY_SPACE_CHAR = "."
    ROW_SPACING = " " * 2
    COL_INDENT = " " * 5
    COL_SPACING = " " * 2
    COL_UNDERLINE_INDENT = " " * 3
    COL_UNDERLINE = "—" * 18

    def __init__(self):
        self.__UI_type = "TERMINAL"
        self.__game = Game(input("Enter player 1's name: "), input("Enter player 2's name: "))
    
    def get_UI_type(self):
        return self.__UI_type
    
    def __get_cords_from_user(self, prompt):

        """Gets a valid coordinate from the user in the form 'row,col' where row and col are integers between 0 and 5 inclusive."""

        valid = False

        min_row_index = MultiClassBoardAttributes.MIN_ROW_INDEX
        max_row_index = MultiClassBoardAttributes.MAX_ROW_INDEX
        
        # regex pattern to check if the user's input is valid
        pattern = fr'^[{min_row_index}-{max_row_index}],[{min_row_index}-{max_row_index}]$'

        while not valid:

            choice = input(prompt)
            if bool(re.match(pattern, choice)):
                valid = True

            else:
                print("Invalid Coordinate. Must be of the form 'r,c' where r and c are integers between 0 and 5 inclusive.")

        # convert the user's input to a tuple of integers of the form (r,c)
        return tuple([int(i) for i in choice.split(",")])
    
    def __display_board(self):

        """Displays the board in the terminal"""

        board = self.__game.get_board_state()
        
        disp_board = []

        for row in board:
            for loc in row:
                if loc.is_empty():
                    disp_board.append(f"{self.EMPTY_SPACE_CHAR}")

                else:
                    # single character representing the colour of the piece
                    disp_board.append(loc.get_colour()[0])
        
        # convert the one dimensional array to a 6x6 two dimensional array
        disp_board = oneD_to_twoD_array(disp_board, MultiClassBoardAttributes.MAX_ROW_INDEX + 1)

        # display the column indexes
        self.__display_col_indexes()

        # displaay the row indexes and the board
        for ind,row in enumerate(disp_board):
            print(f"{ind} | ", end=" ")
            print(self.ROW_SPACING.join(row))

    def __display_col_indexes(self):
        
        """Displays the column indexes of the board in the terminal"""

        print(self.COL_INDENT, end="")
        print(self.COL_SPACING.join([str(i) for i in range(MultiClassBoardAttributes.MAX_ROW_INDEX + 1)]))
        print(self.COL_UNDERLINE_INDENT, end="")
        print(self.COL_UNDERLINE)

    def __display_winner(self):

        """Displays the winner of the game in the terminal"""

        winner = self.__game.get_winning_player()
        print(f"{winner.get_name()} won!")

    def __get_move_type(self):

        """Gets the move type from the user. Either a normal move or a capture move."""

        valid = False
        while not valid:
            
            move_type = input(f"Enter {MultiClassBoardAttributes.NORMAL_MOVE_TYPE} for an ordinary move to an adjacent position or {MultiClassBoardAttributes.CAPTURE_MOVE_TYPE} for a capturing move: ")
            
            if move_type == MultiClassBoardAttributes.NORMAL_MOVE_TYPE or move_type == MultiClassBoardAttributes.CAPTURE_MOVE_TYPE:
                valid = True

            else:
                print("Invalid move type. Please try again.")

        return move_type

    def play_game(self):

        """The main loop of the terminal UI. Handles all events and updates the UI accordingly.
        This is the main public method of the UI class and is called by the main.py file to launch the application."""

        while not self.__game.is_game_over():

            self.__display_board()

            print(f"\n{self.__game.get_current_player_name()}'s turn ({self.__game.get_current_player_colour()}).\n")

            valid = False
            while not valid:

                move_type = self.__get_move_type()

                start_cords = self.__get_cords_from_user("Enter a row and column pair in the format r,c for the piece you want to move: ")
                end_cords = self.__get_cords_from_user("Enter a row and column pair in the format r,c for where you want to move to: ")

                # getting the corresponding GridLocation objects from the game object's board
                start_loc = self.__game.get_board_state()[start_cords[0]][start_cords[1]]
                end_loc = self.__game.get_board_state()[end_cords[0]][end_cords[1]]

                if self.__game.is_legal_move(start_loc, end_loc, move_type):
                    valid = True
                else:
                    print("Invalid move. Please try again.")

            self.__game.make_and_return_move(start_loc, end_loc, move_type)
            
            self.__game.switch_current_player()
            
            # game can only be over after a capture move
            if move_type == MultiClassBoardAttributes.CAPTURE_MOVE_TYPE:
                self.__game.set_game_status()

        # display the final board and the winner
        self.__display_board()
        self.__display_winner()