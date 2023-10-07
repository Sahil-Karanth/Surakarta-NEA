import random
from copy import deepcopy

def oneD_to_twoD_array(lst, width):
    return [lst[i:i+width] for i in range(0, len(lst), width)]

def twoD_to_oneD_array(lst):
    return [item for sublist in lst for item in sublist]

def shuffle_2D_array(arr):
    
    arr_copy = deepcopy(arr)

    arr = twoD_to_oneD_array(arr)
    random.shuffle(arr)
    arr = oneD_to_twoD_array(arr, len(arr_copy[0]))

    return arr


# ! CREDIT TO: https://stackoverflow.com/questions/17985216/simpler-way-to-draw-a-circle-with-tkinter
def create_circle(canvas, x, y, r, fill): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1, fill=fill)


