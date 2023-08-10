import PySimpleGUI as sg

layout = [
    [sg.Button("test", key="abc")]
]

# Create the window
window = sg.Window('Surakarta', layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

    if event == "abc":
        print("test")

window.close()