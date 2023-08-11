import PySimpleGUI as sg


def make_piece_button(key, visible=False):
    
    button = sg.Button(
        button_text="test",
        key=key,
        pad=(0, 0),
        border_width=0,
        button_color=("white", "blue"),  # Changed button_color
        visible=visible)

    return button


loc_button_layout = [
    [make_piece_button("blank", visible=False)],
    [make_piece_button("y", visible=False)],
    [make_piece_button("g", visible=True)]
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