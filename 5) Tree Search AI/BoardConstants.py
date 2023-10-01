class BoardConstants:

    MIN_ROW_INDEX = 0
    MAX_ROW_INDEX = 5
    PLAYER_1_ROWS = (0, 1)
    PLAYER_2_ROWS = (4, 5)
    EDGE_LOCATION_CORDS = ((0, 0), (0, 5), (5, 0), (5, 5))
    PLAYER_1_COLOUR = "y"
    PLAYER_2_COLOUR = "g"
    NUM_STARTING_PIECES_EACH = 2
    ADJACENT_CORD_DIFFS = (1, 2)
    NUM_BOARD_LOOPS = 4
    DRAW_THRESHOLD = 50

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