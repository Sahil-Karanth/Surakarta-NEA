import PySimpleGUI as sg

a = sg.popup_yes_no("You already have a saved game. Do you want to overwrite it?", title="Game Already Saved", keep_on_top=True)

print(a)