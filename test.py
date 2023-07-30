import PySimpleGUI as sg

# The window with the image
layout1 = [[sg.Image(filename='blank_board.png')]]
window1 = sg.Window('Window with image', layout1, no_titlebar=True, location=(100, 100))

# The transparent window with the buttons
layout2 = [[sg.Button('Button 1')], [sg.Button('Button 2')]]
window2 = sg.Window('Window with buttons', layout2, alpha_channel=0.5, no_titlebar=True, location=(200, 200))

while True:  # Event loop
    window, event, values = sg.read_all_windows()
    if window == window2 and event in (sg.WINDOW_CLOSED, 'Exit'):
        break




window1.close()
window2.close()