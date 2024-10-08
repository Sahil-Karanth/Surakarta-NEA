from UI import TerminalUI, GraphicalUI

if __name__ == "__main__":

    valid_ui_type = False

    while not valid_ui_type:
        
        ui_type = input("Enter 't' for terminal UI or 'g' for graphical UI: ")

        if ui_type == 't':
            ui = TerminalUI()
            valid_ui_type = True

        elif ui_type == 'g':
            ui = GraphicalUI()
            valid_ui_type = True

        else:
            print("Invalid input. Please try again.")
    
    ui.play_game()