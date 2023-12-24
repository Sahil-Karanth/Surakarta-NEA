class MultiClassBoardAttributes:

    """This class contains attributes about the Surakarta board that need to be accessed by multiple classes."""

    # can be changed using set_player_colour
    player_1_colour = "yellow"
    player_2_colour = "green"

    # unchanged constants
    DEFAULT_PLAYER_1_COLOUR = "yellow"
    DEFAULT_PLAYER_2_COLOUR = "green"

    NORMAL_MOVE_TYPE = "move"
    CAPTURE_MOVE_TYPE = "capture"

    INNER_LOOP_STRING = "INNER"
    OUTER_LOOP_STRING = "OUTER"
    BOTH_LOOP_STRING = "BOTH"

    MIN_ROW_INDEX = 0
    MAX_ROW_INDEX = 5
    NUM_STARTING_PIECES_EACH = 12




    @staticmethod
    def set_player_colour(colour, player_num):
        if player_num == 1:
            MultiClassBoardAttributes.player_1_colour = colour
        elif player_num == 2:
            MultiClassBoardAttributes.player_2_colour = colour