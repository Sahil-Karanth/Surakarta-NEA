import PySimpleGUI as sg


def make_piece_button(piece, key, visible=False):
    
    button = sg.Button(
        # image_filename=f"pieces/{piece}.png",
        # image_size=(50, 50),
        button_text="test",
        key=key,
        pad=(0, 0),
        border_width=0,
        button_color=(sg.theme_background_color(), sg.theme_background_color()),
        visible=visible)

    return button


x = make_piece_button("blank", "blank", visible=False)
y = make_piece_button("y", "y_key", visible=False)
z = make_piece_button("g", "g_key", visible=True)


loc_button_layout = [
    [x],
    [y],
    [z]
]


# loc_button_layout = [
#     [sg.Button("a", visible=False)],
#     [sg.Button("b", visible=False)],
#     [sg.Button("c")]
# ]


loc_layout = [
    [sg.Column(loc_button_layout)]
]



window = sg.Window('Grid of Columns', loc_layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

window.close()