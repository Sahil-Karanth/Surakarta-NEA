import PySimpleGUI as sg


def make_piece_button(piece_type, key, visible=False):
    return sg.Button("", mouseover_colors="red", image_filename=f"{piece_type}_counter.png", visible=visible, key=key, button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0)



layout = [
    [make_piece_button("blank", "g1", visible=True), make_piece_button("g", "g2", visible=True)],
    [make_piece_button("g", "g3", visible=True), make_piece_button("g", "g4", visible=True)]

]


window = sg.Window('Grid of Columns', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    elif event == "g1":
        window["g1"].update(image_filename="y_counter.png")

    elif event == "g2":
        window["g2"].update(image_filename="y_counter.png")

window.close()