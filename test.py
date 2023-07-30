import PySimpleGUI as sg

# Define button layout
button_layout = [[sg.Button(f'({i+1},{j+1})', key=(i, j)) for j in range(6)] for i in range(6)]

# Define main layout
layout = [
    [sg.Column([[sg.Frame('', button_layout)], [sg.Canvas(key='-CANVAS-', size=(400, 400))]])]
]

# Create the window
window = sg.Window('6x6 Frame of Buttons with Canvas', layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif type(event) is tuple:  # Button click event
        print(f'Button {event} clicked')
        canvas = window['-CANVAS-'].TKCanvas
        canvas.create_oval(10, 10, 50, 50)  # Example of drawing on canvas