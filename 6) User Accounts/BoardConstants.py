class BoardConstants: # ! rename to BoardValues

    player_1_colour = "yellow"
    player_2_colour = "green"

    MIN_ROW_INDEX = 0
    MAX_ROW_INDEX = 5
    PLAYER_1_ROWS = (0, 1)
    PLAYER_2_ROWS = (4, 5)
    EDGE_LOCATION_CORDS = ((0, 0), (0, 5), (5, 0), (5, 5))
    NUM_STARTING_PIECES_EACH = 5
    ADJACENT_CORD_DIFFS = (1, 2)
    NUM_BOARD_LOOPS = 4
    DRAW_THRESHOLD = 50
    SAVED_GAME_STATE_SEPARATOR = "$"
    SAVED_GAME_STATE_EMPTY_CHAR = "."

    OUTER_LOOP_CORDS = [
        (5,2), (4,2), (3,2), (2,2), (1,2), (0,2),
        (2,0), (2,1), (2,2), (2,3), (2,4), (2,5),
        (0,3), (1,3), (2,3), (3,3), (4,3), (5,3),
        (3,5), (3,4), (3,3), (3,2), (3,1), (3,0),
    ]

    INNER_LOOP_CORDS = [
        (4,0), (4,1), (4,2), (4,3), (4,4), (4,5),
        (5,4), (4,4), (3,4), (2,4), (1,4), (0,4),
        (1,5), (1,4), (1,3), (1,2), (1,1), (1,0),
        (0,1), (1,1), (2,1), (3,1), (4,1), (5,1),
    ]


    @staticmethod
    def set_player_colour(colour, player_num):
        if player_num == 1:
            BoardConstants.player_1_colour = colour
        elif player_num == 2:
            BoardConstants.player_2_colour = colour