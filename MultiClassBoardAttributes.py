class MultiClassBoardAttributes:

    """This class contains attributes about the Surakarta board that need to be accessed by multiple classes.
    
    ####################################################################
    GOOD CODING STYLE: Use of constants
    ####################################################################

    """

    # can be changed using set_player_colour
    player_1_colour = "yellow"
    player_2_colour = "green"

    # unchanged constants
    DEFAULT_PLAYER_1_COLOUR = "yellow"
    DEFAULT_PLAYER_2_COLOUR = "green"

    NORMAL_MOVE_TYPE = "move"
    CAPTURE_MOVE_TYPE = "capture"

    INNER_TRACK_STRING = "INNER"
    OUTER_TRACK_STRING = "OUTER"
    BOTH_TRACK_STRING = "BOTH"

    EASY_AI_NAME = "Easy AI"
    MEDIUM_AI_NAME = "Medium AI"
    HARD_AI_NAME = "Hard AI"

    MIN_ROW_INDEX = 0
    MAX_ROW_INDEX = 5
    
    NUM_STARTING_PIECES_EACH = 12

    @staticmethod
    def set_player_colour(colour, player_num):

        """sets the colour of a player's pieces. Used by the GUI to change the colour of the pieces for a logged in user."""

        if player_num == 1:
            MultiClassBoardAttributes.player_1_colour = colour
        elif player_num == 2:
            MultiClassBoardAttributes.player_2_colour = colour