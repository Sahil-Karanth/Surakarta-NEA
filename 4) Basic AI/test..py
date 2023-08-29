import PySimpleGUI as sg

layout = [[sg.Button('Unclickable Button', disabled=True, button_color=('white', 'red'))]]

window = sg.Window('Window Title', layout)

while True: 
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

window.close()