import PySimpleGUI as sg

# Layout for main window content
layout = [
    [sg.Text("Main Window Content")],
    [sg.Button("Ok")]    
]

# Layout for top message 
top_layout = [
    [sg.Text("This is a short message at the top")]
]

# Full layout
full_layout = [
    [sg.Column(top_layout, size=(500,30), pad=(0,0), background_color='blue')], 
    [sg.Column(layout)]
]

window = sg.Window("Window Title", full_layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
        
window.close()