from BoardConstants import BoardConstants

class Player:

    def __init__(self, piece_colour):
        self.__piece_colour = piece_colour
        self.__piece_count = BoardConstants.NUM_STARTING_PIECES_EACH

    def get_colour(self):
        return self.__piece_colour
    
    def get_piece_count(self):
        return self.__piece_count
    
    def remove_piece(self):
        self.__piece_count -= 1
        if self.__piece_count < 0:
            raise ValueError("Player has no pieces left, cannot remove piece")
        
    def add_piece(self):

        """Adds a piece to the player's piece count. Only used to return a piece to a player after a move is undone."""

        self.__piece_count += 1
        if self.__piece_count > BoardConstants.NUM_STARTING_PIECES_EACH:
            raise ValueError("Player has too many pieces, cannot add piece")
    

class HumanPlayer(Player):

    def __init__(self, name, piece_colour):
        super().__init__(piece_colour)
        self.__name = name

    def get_name(self):
        return self.__name
    

class EasyAIPlayer(Player):

    def __init__(self, piece_colour):
        super().__init__(piece_colour)
        self.__name = "Easy AI"

    def get_name(self):
        return self.__name
    
    def get_move(self, board):
        
        for row in board.get_board_state():
            for loc in row:
                if (loc.get_colour() == self.get_colour()):
                    move = self.board.get_capture_with(loc)

                    if move:
                        return move
                    
                    move = self.board.get_move_with(loc)
                    
                

                    

    

class MediumAIPlayer(Player):
    
    def __init__(self, piece_colour):
        super().__init__(piece_colour)
        self.__name = "Medium AI"
    def get_name(self):
        return self.__name
    
class HardAIPlayer(Player):
        
    def __init__(self, piece_colour):
        super().__init__(piece_colour)
        self.__name = "Hard AI"

    def get_name(self):
        return self.__name


    