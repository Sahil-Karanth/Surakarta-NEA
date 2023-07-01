class Terminal_UI:
    
    def __init__(self):
        self.__UI_type = "TERMINAL"

    def get_UI_type(self):
        return self.__UI_type
    
    def get_user_piece_to_move(self):
        choice = input("Enter a row and column pair in the format r,c for the piece you want to move: ")
        return choice
    
    def get_user_piece_moving_to(self):
        choice = input("Enter a row and column pair in the format r,c for where you want to move to: ")
        return choice
    
    

