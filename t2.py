import PySimpleGUI as sg



loc_button_layout = [
    [sg.Button("a", visible=False)],
    [sg.Button("b", visible=False)],
    [sg.Button("c")]
]





loc_layout = [
    [sg.Column(loc_button_layout)]
]


window = sg.Window('Grid of Columns', loc_layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

window.close()






