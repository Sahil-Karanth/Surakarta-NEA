from UI import Terminal_UI, Graphical_UI

if __name__ == "__main__":

    # valid_ui_type = False
    # while not valid_ui_type:
    #     ui_type = input("Enter 't' for terminal UI or 'g' for graphical UI: ")

    #     if ui_type == 't':
    #         ui = Terminal_UI()
    #         valid_ui_type = True

    #     elif ui_type == 'g':
    #         ui = Graphical_UI()
    #         valid_ui_type = True

    #     else:
    #         print("Invalid input. Please try again.")

    ui = Graphical_UI()
    
    ui.play_game()

