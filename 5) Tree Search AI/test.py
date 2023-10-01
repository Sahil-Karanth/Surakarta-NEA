import PySimpleGUI as sg
from PIL import ImageTk, Image

circle_visible = False

def draw_circle(canvas):
    global circle_visible
    if circle_visible:
        canvas.delete('circle')
        circle_visible = False
    else:
        canvas.create_oval(50, 50, 150, 150, fill='red', tags='circle')
        circle_visible = True

layout = [
    [sg.Canvas(size=(500, 500), key='-CANVAS-')],
    [sg.Button('Toggle Circle', key='-BUTTON-')]
]

window = sg.Window('Circle Drawing', layout, finalize=True, keep_on_top=True)

canvas = window['-CANVAS-'].TKCanvas
image_path = 'blank_board.png'
image = Image.open(image_path)
image.thumbnail((500, 500))  # Resize the image to fit the canvas
background_img = ImageTk.PhotoImage(image)
canvas.create_image(0, 0, image=background_img, anchor='nw')

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == '-BUTTON-':
        draw_circle(canvas)

window.close()